from decimal import Decimal
from dateutil.relativedelta import relativedelta

# rate and tax  needs to be Decimal, investment.amount is registred as Decimal, so it only supports operations with other Decimals
# rate = 0,52% per month

def get_growth_rate():
    rate = Decimal('0.0052')
    return rate

def get_tax_rate(months):
    if months < 12:
        return Decimal('0.225')
    elif 12 <= months < 24:
        return Decimal('0.185')
    else:
        return Decimal('0.150')

def get_month_diff(start_date,end_date):
    """
    Return the diference in months within any 2 given dates
    :param start_date:
    :param end_date:
    :return:
    """
    delta_time = relativedelta(end_date,start_date) # Time difference between dates
    months = (delta_time.years or 0)*12 + (delta_time.month or 0)
    return months

def calculate_expected_balance(rate, amount, months):
    """
    Calculate an expected balance using composite gain
    :param rate: growth rate per month
    :param amount: inicial investment
    :param months: months passed
    :return: The total composite amount
    """
    percentage_gains = (Decimal(1) + rate) ** Decimal(months)
    total_amount = amount * percentage_gains
    return total_amount