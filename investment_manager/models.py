from django.db import models

# Create your models here.
class Owner(models.Model):
    """
    Pt:
    Modelo dos donos de cada investimento

    Relations : Many to one - Investments

    Args:
        name (str): name of the owner
        birthday(dateTime.date): Birthday date of the owner
    """
    name = models.CharField(max_length=100, blank=False,null=False)
    birthday = models.DateField(help_text="Birthday date of the owner")

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Birthday date: {self.birthday}")

class Investment(models.Model):
    """
    Pt:
    Modelo dos investimentos. Cada investimento possui um investidor (Owner)

    Relations: Many to one - Owner

    Args:
        owner (Owner): The owner of the investment
        amount (float): The amount of the investment
        creation_date (dateTime.date): Date of creation
        withdraw_date (dateTime.date): Date of withdraw
    """
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    creation_date = models.DateField(null=False)
    withdraw_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return (f"Owner: {self.owner.name}\n"
                f"Amount: {self.amount}\n"
                f"Investment date: {self.creation_date}\n"
                f"Withdraw date: {self.withdraw_date}")
