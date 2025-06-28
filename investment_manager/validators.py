from datetime import datetime, date

from rest_framework.exceptions import ValidationError

"""
File containing validation methods used in serializers
"""

def validate_expected_date(investment_date, expected_date):
    """
    Pt:
    Função para validar se a data esperada é menor que a data de investimento

    Args:
        investment_date (datetime.date): Date of creation of the investment
        expected_date (datetime.date): Expected date to be compared

    Raises:
        ValidationError
    """
    if expected_date < investment_date:
        raise ValidationError("Expected date is before investment date")

def parse_expected_date(expected_date_string):
    """
    Pt:
    Função usada para formatar uma string em datetime.date, se o formato for inválido, a checagem falha

    Args:
        expected_date_string(str): String to be formatted

    Returns:
        Formatted date from string

    Raises:
        ValidationError
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

    Raises:
        ValidationError
    """
    if amount <= 0:
        raise ValidationError("Amount can't be negative nor 0")

def validate_investment_creation_date(investment_creation_date):
    """
    Pt:
    Valida se a data de investimento não é no futuro

    Args:
        investment_creation_date(datetime.date): Date of investment

    Raises:
        ValidationError
    """
    if investment_creation_date > date.today():
        raise ValidationError("Date of investment can't be in future")

def validate_withdraw_date(investment_date, withdraw_date):
    """
    Validates if withdraw input is not future

    Args:
        investment_date: Creation date of the investment
        withdraw_date: input date of withdrawal
    Raises:
        ValidationError
    """
    if withdraw_date <= date.today():
        validate_expected_date(investment_date,withdraw_date)
    else:
        raise  ValidationError("Date of withdraw can't be in future")

def check_if_already_withdrawn(investment_withdraw_date):
    """
    Validates if investment is already withdrawn
    Args:
        investment_withdraw_date: date of withdrawal
    Raises:
         ValidationError
    """
    if investment_withdraw_date:
        raise ValidationError("Investment already withdrawn")
