from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from  rest_framework.test import APITestCase

from investment_manager.models import Owner
from investment_manager.serializers import OwnerSerializer


class OwnerTest(APITestCase):
    """
    Test for owner CRUD API endpoint
    """

    def setUp(self):

        self.user= User.objects.create_superuser(username='admin',password='admin')
        self.url = reverse('Owners-list')
        self.client.force_authenticate(user = self.user)

        #Set up test objects
        self.mock_owner_1= Owner.objects.create(
            name = "As long as its a one hundred caracters long",
            birthday = '2004-08-12'
        )

        self.mock_owner_2 = Owner.objects.create(
            name= "As long as its a one hundred caracters long",
            birthday='2005-08-12'
        )

    def test_get_owner_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_owner_by_id(self):
        response = self.client.get(self.url+'1/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        owner_data = Owner.objects.get(pk=1)
        owner_data_serialized = OwnerSerializer(instance=owner_data).data
        self.assertEqual(response.data,owner_data_serialized)

    def test_delete_owner(self):
        response = self.client.delete(self.url+'2/')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_post_valid_owner(self):
        post_data = {
            'name':'As long as a hundred caracters',
            'birthday': '2000-12-31'
        }
        response = self.client.post(self.url,data = post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_owner_name(self):
        post_data = {
            'name':'a',
            'birthday':'2000-12-31'
        }
        response = self.client.post(self.url,data = post_data)
        self.assertIn("Invalid Name",response.data['name'][0])
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_owner_birthday_format(self):
        post_data = {
            'name':'abc',
            'birthday':'000-12-31'
        }
        response = self.client.post(self.url,data = post_data)
        self.assertIn("YYYY-MM-DD",response.data['birthday'][0])
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    def test_post_invalid_owner_age(self):
        post_data = {
            'name':'abc',
            'birthday': date.today()
        }
        response = self.client.post(self.url,data = post_data)
        self.assertIn("Age", response.data['birthday'][0])
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

