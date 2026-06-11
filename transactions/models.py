from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User,related_name='split_groups')
    base_currency = models.CharField(max_length=5, default='USD')

    
    def __str__(self):
        return self.name
class Expense(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    currency_used = models.CharField(max_length=5)
    converted_amount = models.DecimalField(max_digits=12, decimal_places=2)

class ExpenseSplit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    