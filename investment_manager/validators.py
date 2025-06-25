from datetime import datetime, date

from rest_framework.exceptions import ValidationError

"""
File containing validation methods used in serializers
"""

def validate_expected_date(investment_date, expected_date):
    """
    Pt:
    Método para validar se a data esperada é menor que a data de investimento

    Args:
        investment_date (datetime.date): Date of creation of the investment
        expected_date (datetime.date): Expected date to be compared
    """
    if expected_date < investment_date:
        raise ValidationError("Expected date is before investment date")

def parse_expected_date(expected_date_string):
    """
    Pt:
    Método usado para formatar uma string em datetime.date, se o formato for inválido, a checagem falha

    Args:
        expected_date_string(str): String to be formatted

    Returns:
        Formatted date from string or raises an error
    """
    try:
        parsed_expected_date = datetime.strptime(expected_date_string,'%Y-%m-%d').date()
        return parsed_expected_date
    except ValueError:
         raise ValidationError("Invalid format. Should be 'YYYY-MM-DD'")

def validate_amount(amount):
    """
    Pt:
    Simplesmente valida se o valor investido é menor que 0

    Args:
        amount(float): Initial investment amount
    """
    if amount < 0:
        raise ValidationError("Amount can't be negative")

def validate_investment_creation_date(investment_creation_date):
    """
    Pt:
    Valida se a data de investimento não é no futuro

    Args:
        investment_creation_date(datetime.date): Date of investment
    """
    if investment_creation_date > date.today():
        raise ValidationError("Date of investment can't be in future")


