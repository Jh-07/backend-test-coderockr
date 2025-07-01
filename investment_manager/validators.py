import re
from datetime import datetime, date

from rest_framework.exceptions import ValidationError

from investment_manager.utils import get_month_diff, format_date

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

def validate_owner_birthday(birthday):
    """
    Validates owner birthday
    Args:
        birthday: Birthday date
    Raises:
         ValidationError
    """
    age = get_month_diff(birthday,date.today())//12
    if age <= 12:
        raise ValidationError("Age should be 13 or higher")

def validate_owner_name(name):
    """
    Validates owner name
    Args:
        name: Owner's name
    Raises:
         ValidationError
    """
    regex = r"[A-Za-zÀ-ÿ\s]{3,100}"
    if not re.fullmatch(regex,name):
        raise ValidationError("Invalid Name")

