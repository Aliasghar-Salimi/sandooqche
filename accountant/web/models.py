from django.db import models
from django.contrib.auth.models import User
import re
# Create your models here.

class Expense(models.Model):
    text = models.CharField(max_length=250)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        text = "'{}' {}|\"{}\" {}".format(self.user, self.date,self.text, self.amount)
        pattern = r'(\+00:00)'
        newtext = re.sub(pattern,"" , text)
        return newtext

class Income(models.Model):
    text = models.CharField(max_length=200)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        text = "'{}' {}|\"{}\" {}".format(self.user, self.date,self.text, self.amount)
        pattern = r'(\+00:00)'
        newtext = re.sub(pattern,"" , text)
        return newtext    

