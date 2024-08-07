from django.contrib import admin
from .models import User, Income, Expense

admin.site.register(User)
admin.site.register(Income)
admin.site.register(Expense)