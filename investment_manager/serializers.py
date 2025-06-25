
from datetime import date,datetime

from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from investment_manager import  validators
from investment_manager.models import Owner, Investment


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
    class Meta:
        model = Investment
        fields = '__all__'

    def get_expected_balance(self, investment):
        """
        Pt:
        Retorna o campo expected_balance (total de dinheiro esperado dado uma data maior que
        a data de criação do investimento) no JSON da resposta

        Args:
            investment (Investment): Investment model

        Returns:
            Expected balance for the especific date from the investment creation date
        """
        request = self.context.get('request') #Recebe o request do contexto do serializer
        expectation_date = date.today()
        if request:
            expectation_date_str = request.query_params.get('expectation_date') #Recebe a data passada na URL e confere se a formatação está correta (ano-mes-dia)
            expectation_date = validators.parse_expected_date(expectation_date_str)
            validators.validate_expected_date(investment.creation_date,expectation_date)

        rate = 0.00052 #0.52%

        delta_time = relativedelta(expectation_date,investment.creation_date) # Diferença de tempo entre a data de criação do investimento e a data esperada
        months = delta_time.years*12 + delta_time.month #Observação: Relativedelta ,quando passada duas datas, retorna um objeto com arumentos de ano, mês e dias de diferença
        percentage_gains =  (1+rate) ** months
        expected_balance = investment.amount * percentage_gains

        return round(expected_balance,2)