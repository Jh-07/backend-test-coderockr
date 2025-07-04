from datetime import datetime, date
from rest_framework.decorators import action
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from investment_manager.models import Investment, Owner
from investment_manager.serializers import InvestmentSerializer, OwnerSerializer


class InvestmentViewSet(viewsets.ModelViewSet):
    """
    Enable CRUD for Investments
    """
    queryset = Investment.objects.all().order_by('-creation_date','-id')
    serializer_class = InvestmentSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns a list of investments, can be all of them or filter by the owner's name
        """
        queryset =self.get_queryset()
        owner = self.request.query_params.get('owner')
        if owner:
            queryset = Investment.objects.all().filter(owner__name__icontains=owner) # Filter by owner name. Since owner is a Foreign key, owner__name shoud be refered to the field (name) of the referenced object (owner)
            if not queryset:
                return Response(data={"No investments found for this query"} ,status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(data= serializer.data, status=status.HTTP_200_OK)

    # @action registers the url as basename-action, in this case investment-withdraw
    # I don't undestand what detail parameter means, look it up.
    # Answer: detail = True means this  receives a parameter to query a single instance (usualy is ID)
    # detail = False means this action is aplied to a list of objects(queryset). If it where this case, you should deal with each instance separetly (using a for i.e) or passing many= True on  get.serializer if it's all the same treatment
    @action(detail = True, methods=['put'],url_path='withdraw')
    def withdraw(self,request,pk = None):
        """
        Creates an PUT only endpoint named 'withdraw'. If there is no body, passes today's date
        """
        investment = generics.get_object_or_404(Investment,pk=pk)
        withdraw_date_str = request.data.get('withdraw_date')
        if withdraw_date_str:
            try:
                #I don't understand why withdraw_date is 'not being used'
                #Answer: It seems to be an IDE bug, withdraw date is used correctly
                withdraw_date = datetime.strptime(withdraw_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(data={"detail": "Invalid format. Should be 'YYYY-MM-DD'"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            withdraw_date = date.today()
        # I don't undestand this part either, look it up [lines 49-53]
        # Answer: This serializes the PUT body data to the Investment instance chosen.
        # In this case, partialy [line 55], this means it can pass just parts of the investment object(only withdraw_date in the case) .
        serializer = self.get_serializer(
            investment,
            data = {'withdraw_date': withdraw_date},
            partial = True
        )
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_200_OK)


class OwnerViewSet(viewsets.ModelViewSet):
    """
    Enables CRUD for Owners
    """
    queryset = Owner.objects.all().order_by('id', 'name')
    serializer_class = OwnerSerializer
