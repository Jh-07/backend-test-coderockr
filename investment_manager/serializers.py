
from datetime import date
from decimal import Decimal
from rest_framework import serializers
from rest_framework.serializers import  SkipField
from rest_framework.exceptions import ValidationError

from investment_manager import  validators
from investment_manager.models import Owner, Investment
from investment_manager.utils import get_month_diff, calculate_expected_balance, get_growth_rate, get_tax_rate
from investment_manager.validators import parse_expected_date


class OwnerSerializer(serializers.ModelSerializer):
    """
    Pt:
    Serializador da classe/modelo Owner
    Serializa todos os campos
    """

    class Meta:
        model = Owner
        fields = '__all__'


class InvestmentSerializer(serializers.ModelSerializer):
    """
    Pt:
    Serializador da classe/modelo Investment
    Serializa todos os campos
    """



    expected_balance = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    gains = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        fields = '__all__'

    def validate(self, data):
        creation_date = data.get('creation_date')
        amount = data.get('amount')
        withdraw_date = data.get('withdraw_date')

        validators.validate_amount(amount)
        validators.validate_investment_creation_date(creation_date)
        if withdraw_date:
            validators.validate_expected_date(creation_date, withdraw_date)
        return data

    def get_gains(self,investment):
        if not investment.withdraw_date:
            return None
        else:
            months = get_month_diff(investment.creation_date, investment.withdraw_date)
            rate = get_growth_rate()
            total_amount = calculate_expected_balance(rate, investment.amount, months)
            return total_amount - investment.amount


    def get_tax(self,investment):
        if not investment.withdraw_date:
            return None
        else:
            months = get_month_diff(investment.creation_date, investment.withdraw_date)
            gains = self.get_gains(investment)
            tax = get_tax_rate(months)
            return gains * tax

    def get_expected_balance(self, investment):
        """
        Pt:
        Retorna o campo expected_balance (total de dinheiro esperado dado uma data maior que
        a data de criação do investimento) no JSON da resposta

        Args:
            investment (Investment): Investment model

        Returns:
            Expected balance for the especific date from the investment creation date or
            Only the gains if the investment is withdrawn or
            A string explaining why is not a valid request
        """
        expectation_date = date.today() #By default, expectation date is today
        request = self.context.get('request')
        if request:
            expectation_date_str = request.query_params.get('expectation_date')
            if expectation_date_str:
                try:
                    expectation_date = parse_expected_date(expectation_date_str)
                except ValidationError:
                    return "Invalid expected_date format (use YYYY-MM-DD)"
        if expectation_date < investment.creation_date:
            return "Invalid expected date. Date is before the investment"


        if investment.withdraw_date: #If there is a withdrawal date, then  don't show this field
            return None
        else: #Else, return the amount + gains expected
            months = get_month_diff(investment.creation_date,expectation_date)
            total_amount = calculate_expected_balance(get_growth_rate(), investment.amount,months)
            return Decimal(total_amount)



