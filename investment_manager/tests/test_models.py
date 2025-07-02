from datetime import date, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from  rest_framework.test import APITestCase

from investment_manager.models import Owner, Investment
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
            name = "Jonathas Martins",
            birthday = '2004-08-12'
        )

        self.mock_owner_2 = Owner.objects.create(
            name= "Regildo Silva",
            birthday='2005-08-12'
        )

        self.mock_owner_3 = Owner.objects.create(
            name="Maria Eliane",
            birthday='2000-08-12'
        )

        self.mock_owner_4 = Owner.objects.create(
            name="João Pedro",
            birthday='1980-08-12'
        )

    def test_get_owner_list(self):
        """
        Tests GET requests for all owners
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_owner_by_id(self):
        """
        Tests GET requests for an especific owner
        """
        response = self.client.get(self.url+'1/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        owner_data = Owner.objects.get(pk=1)
        owner_data_serialized = OwnerSerializer(instance=owner_data).data
        self.assertEqual(response.data,owner_data_serialized)

    def test_delete_owner(self):
        """
        Tests DELETE request
        :return:
        """
        response = self.client.delete(self.url+'2/')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_post_valid_owner(self):
        """
        Tests valid POST request
        :return:
        """
        post_data = {
            'name':'As long as a hundred caracters',
            'birthday': '2000-12-31'
        }
        response = self.client.post(self.url,data = post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_owner_name(self):
        """
        Tests POST invalid request: name field
        :return:
        """
        post_data = {
            'name':'a',
            'birthday':'2000-12-31'
        }
        response = self.client.post(self.url,data = post_data)
        self.assertIn("Invalid Name",response.data['name'][0])
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_owner_birthday_format(self):
        """
        Tests POST invalid request: date format
        :return:
        """
        post_data = {
            'name':'abc',
            'birthday':'000-12-31'
        }
        response = self.client.post(self.url,data = post_data)
        self.assertIn("YYYY-MM-DD",response.data['birthday'][0])
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    def test_post_invalid_owner_age(self):
        """
        Test POST invalid request: young age
        :return:
        """
        post_data = {
            'name':'abc',
            'birthday': date.today()
        }
        response = self.client.post(self.url,data = post_data)
        self.assertIn("Age", response.data['birthday'][0])
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class InvestmentTest(APITestCase):
    """
    Tests investment related endpoints
    """

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.url_crud = reverse('Investments-list')
        self.url_withdraw_3 = reverse('Investments-withdraw', kwargs={'pk':3})
        self.url_withdraw_4 = reverse('Investments-withdraw', kwargs={'pk':4})
        self.client.force_authenticate(user=self.user)


        #Set up test owners
        self.mock_owner_1= Owner.objects.create(
            name = "Jonathas Martins",
            birthday = '2004-08-12'
        )

        self.mock_owner_2 = Owner.objects.create(
            name= "Regildo Silva",
            birthday='2005-08-12'
        )

        self.mock_owner_3 = Owner.objects.create(
            name="Maria Eliane",
            birthday='2000-08-12'
        )

        self.mock_owner_4 = Owner.objects.create(
            name="João Pedro",
            birthday='1980-08-12'
        )

        #Set up mock objects
        self.mock_investment_1 = Investment.objects.create(
            owner = self.mock_owner_1,
            amount = 3000.00,
            creation_date = '2002-07-23',
            withdraw_date = None,
        )

        self.mock_investment_2 = Investment.objects.create(
            owner = self.mock_owner_1,
            amount = 1000.00,
            creation_date = '2004-07-23',
            withdraw_date = '2005-09-11',
        )

        self.mock_investment_3 = Investment.objects.create(
            owner = self.mock_owner_2,
            amount = 400.00,
            creation_date = '1985-11-29',
            withdraw_date = '2000-10-05',
        )

        self.mock_investment_4 = Investment.objects.create(
            owner = self.mock_owner_3,
            amount = 230.00,
            creation_date = '2002-07-23',
            withdraw_date = None,
        )

        self.mock_investment_5 = Investment.objects.create(
            owner = self.mock_owner_4,
            amount = 50000.00,
            creation_date = '2016-02-12',
            withdraw_date = '2018-01-15',
        )

    def test_get_investment_list(self):
        """
        Tests GET requests for all investments
        """
        response = self.client.get(self.url_crud)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_investmentf_by_id(self):
        """
        Tests GET requests for an especific investment
        """
        response = self.client.get(self.url_crud+'3/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_investment_by_owner_name(self):
        """
        Tests investment search by owner name
        :return:
        """
        response = self.client.get(self.url_crud+'?owner=Jo')
        print(response.data)
        for investment in response.data:
            print(investment['owner_name'])
            self.assertIn(investment['owner_name'], ["Jonathas Martins" ,"João Pedro"])

    def test_delete_investment(self):
        """
        Tests DELETE request
        :return:
        """
        response = self.client.delete(self.url_crud+'2/')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_post_valid_investment(self):
        """
        Tests valid POST request
        :return:
        """
        post_data = {
            'owner':self.mock_owner_2.id,
            'amount': 2000,
            'creation_date': '2001-06-05',
        }
        response = self.client.post(self.url_crud,data = post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_investment_amount(self):
        """
        Tests invalid POST request : amount
        :return:
        """

        post_data = {
            'owner':self.mock_owner_2.id,
            'amount': -2000,
            'creation_date': '2001-06-05',
        }
        response = self.client.post(self.url_crud,data=post_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("Amount",response.data['amount'][0])

    def test_post_invalid_investment_creation_date(self):
        """
        Tests invalid POST request : creation_date at future
        :return:
        """
        tomorrow = date.today() + timedelta(days=1)
        tomorrow_str = str(tomorrow)
        post_data = {
            'owner':self.mock_owner_2.id,
            'amount': 2000,
            'creation_date': tomorrow_str,
        }
        response = self.client.post(self.url_crud,data=post_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("future",response.data['creation_date'][0])

    def test_post_invalid_investment_withdraw_before_creation(self):
        """
        Tests invalid POST request : withdraw_date
        :return:
        """
        post_data = {
            'owner':self.mock_owner_2.id,
            'amount': 2000,
            'creation_date': '2000-01-02',
            'withdraw_date': '2000-01-01'
        }
        response = self.client.post(self.url_crud,data=post_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        # Validation errors raised inside the general validate() method are returned under the 'non_field_errors' key.
        self.assertIn("before",response.data['non_field_errors'][0])

    def test_put_invalid_investment_already_withdrawn(self):
        """
        Tests invalid PUT request to withdraw endpoint : withdraw an investment that is already withdrawn
        :return:
        """
        put_data = {
            'withdraw_date': '2000-01-01'
        }
        response = self.client.put(self.url_withdraw_3,data=put_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("already withdrawn",response.data['non_field_errors'][0])


    def test_put_invalid_investment_withdraw_future(self):
        """
        Tests invalid PUT request to withdraw endpoint: withdraw date at future
        :return:
        """
        tomorrow = date.today() + timedelta(days=1)
        tomorrow_str = str(tomorrow)
        put_data = {
            'withdraw_date': tomorrow_str
        }

        response = self.client.put(self.url_withdraw_4, data=put_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("future", response.data['non_field_errors'][0])

    def test_put_investment_withdraw_today(self):
        """
        Tests PUT withdraw endpoint without body: withdraw_date should save as today
        :return:
        """
        response = self.client.put(self.url_withdraw_4, date={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.url_crud + '4/')
        registred_date = response.data['withdraw_date']
        today = str(date.today())
        self.assertEqual(today, registred_date)