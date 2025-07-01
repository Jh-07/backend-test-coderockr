
from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from investment_manager import  validators
from investment_manager.models import Owner, Investment
from investment_manager.utils import get_month_diff, calculate_expected_balance, get_growth_rate, get_tax_rate, \
    quantize_decimals, format_date


class OwnerSerializer(serializers.ModelSerializer):
    """
    Pt:
    Serializador da classe/modelo Owner
    Serializa todos os campos
    """

    class Meta:
        model = Owner
        fields = '__all__'

    def validate_name(self,name):
        validators.validate_owner_name(name)
        return name

    def validate_birthday(self,birthday):
        validators.validate_owner_birthday(birthday)
        return birthday


class InvestmentSerializer(serializers.ModelSerializer):
    """
    Pt:
    Serializador da classe/modelo Investment
    Serializa todos os campos além dos campos derivativos expected_balance, tax , total_gains e net_gains.
    """

    ### Derivative fields
    #Option 1:
    owner_name = serializers.CharField(source='owner.name', read_only=True) # This only shows the owner name (and its ID by default)

    # Option 2:
    # owner = OwnerSerializer(read_only=True) # Owner is nested with the investment, so it shows the entire related instance
    expected_balance = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    total_gains = serializers.SerializerMethodField()
    net_gains = serializers.SerializerMethodField()
    ###

    class Meta:
        model = Investment
        fields = '__all__'

    # These individual validations are only triggred if the field is in the body. Make sure that these fields are NOT REQUIRED
    def validate_creation_date(self,creation_date):
        """
        Validates creation_date individualy
        """
        validators.validate_investment_creation_date(creation_date)
        return creation_date

    def validate_amount(self,amount):
        """
        Validates amount individualy
        """
        validators.validate_amount(amount)
        return amount

    # Use this method if you want to validate required fields or especial cases like this one:
    # withdraw date is compared to the user input creation date if exists, if not it will be compared to the current object creatioon date
    def validate(self, data):
        """
        Validate user inputs
        """
        creation_date = data.get('creation_date')
        withdraw_date = data.get('withdraw_date')

        if withdraw_date:
            investment = getattr(self, 'instance', None)
            validators.check_if_already_withdrawn(investment.withdraw_date)
            if creation_date:
                validators.validate_withdraw_date(creation_date, withdraw_date)
            else:
                validators.validate_withdraw_date(investment.creation_date, withdraw_date)

        return data

    def to_representation(self, investment):
        """
        Serialize fields that are relevant.
        If there is a withdrawal, then there is no need to show expected balance,
        else there is no need to show the gains or taxation
        """
        rep = super().to_representation(investment)

        if investment.withdraw_date:
            rep.pop('expected_balance',None)
        else:
            rep.pop('tax',None)
            rep.pop('total_gains',None)
            rep.pop('net_gains',None)
        return rep

    def get_total_gains(self,investment):
        """
        Creates a field of total gains
        """
        if not investment.withdraw_date:
            return None
        else:
            months = get_month_diff(investment.creation_date, investment.withdraw_date)
            rate = get_growth_rate()
            total_amount = calculate_expected_balance(rate, investment.amount, months)
            return quantize_decimals(total_amount - investment.amount)

    def get_net_gains(self,investment):
        """
        Shows net gains (total gains - taxes)
        """
        if not investment.withdraw_date:
            return None
        total_gains =self.get_total_gains(investment)
        tax = self.get_tax(investment)
        return quantize_decimals(total_gains - tax)

    def get_tax(self,investment):
        """
        Shows how mutch tax was paid on withdraw
        """
        if not investment.withdraw_date:
            return None
        else:
            months = get_month_diff(investment.creation_date, investment.withdraw_date)
            gains = self.get_total_gains(investment)
            tax = get_tax_rate(months)
            return quantize_decimals(gains * tax)

    def get_expected_balance(self, investment):
        """
        Pt:
        Retorna o campo expected_balance (total de dinheiro esperado dado uma data maior que
        a data de criação do investimento) no JSON da resposta

        Args:
            investment (Investment): Investment model

        Returns:
            Expected balance for the especific date from the investment creation date as a string or
            None, if the investment is already withdrawn or
            A string explaining why is not a valid request
        """

        if investment.withdraw_date: #If there is a withdrawal date, then this field returns None
            return None

        expectation_date = date.today() #By default, expectation date is today
        request = self.context.get('request')
        if request:
            expectation_date_str = request.query_params.get('expectation_date')
            if expectation_date_str:
                try:
                    expectation_date = format_date(expectation_date_str)
                except ValidationError:
                    return "Invalid expected_date format (use YYYY-MM-DD)"
        if expectation_date < investment.creation_date:
            return "Invalid expected date. Date is before the investment"

        months = get_month_diff(investment.creation_date,expectation_date)
        total_amount = calculate_expected_balance(get_growth_rate(), investment.amount,months)
        return quantize_decimals(total_amount)



