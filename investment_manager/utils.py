from datetime import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import ValidationError

# rate and tax  needs to be Decimal, investment.amount is registred as Decimal, so it only supports operations with other Decimals
# rate = 0,52% per month

def get_growth_rate():
    rate = Decimal('0.0052')
    return rate

def get_tax_rate(months):
    """
    Get tax rate depending on how many months of investments
    """
    tax_rates = [
        '0.225',
        '0.185',
        '0.150'
    ]
    if months < 12:
        return Decimal(tax_rates[0])
    elif 12 <= months < 24:
        return Decimal(tax_rates[1])
    else:
        return Decimal(tax_rates[2])

def get_month_diff(start_date,end_date):
    """
    Return the diference in months within any 2 given dates
    Args:
        start_date:
        end_date:
    Returns:
        number of months
    """
    delta_time = relativedelta(end_date,start_date) # Time difference between dates
    months = (delta_time.years or 0)*12 + (delta_time.month or 0)
    return months

def calculate_expected_balance(rate, amount, months):
    """
    Calculate an expected balance using composite gain

    Args:
        rate: growth rate per month
        amount: inicial investment
        months: months passed
    Returns:
        The total composite amount
    """
    percentage_gains = (Decimal(1) + rate) ** Decimal(months)
    total_amount = amount * percentage_gains
    return quantize_decimals(total_amount)

def format_date(date_str):
    """
       Pt:
       Função usada para formatar uma string em datetime.date, se o formato for inválido, a checagem falha

       Args:
           date_str(str): String to be formatted

       Returns:
           Formatted date from string

       Raises:
           ValidationError
       """
    try:
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return parsed_date
    except ValueError:
        raise ValidationError("Invalid format. Should be 'YYYY-MM-DD'")


def quantize_decimals(decimal):
    return decimal.quantize(Decimal('0.01'))