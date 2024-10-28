# Copyright 2024 dhannon
from django import forms
from .models import Employee, Expense, Income

class EmployeeForm(forms.ModelForm): #Testing merge conflict
    class Meta:
        model = Employee
        fields = ['name', 'salary']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']
