from django.contrib import admin
from .models import Expense
from .models import Income
# Register your models here.

admin.site.register(Expense)
admin.site.register(Income)
