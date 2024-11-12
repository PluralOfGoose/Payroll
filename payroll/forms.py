'''# Copyright 2024 dhannon
from django import forms
from .models import Employee, Expense, Income

# test dhannon
class EmployeeForm(forms.ModelForm): #Testing merge conflict
main
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
        fields = ['source', 'amount', 'date']'''

#copyright 2024 PluralofGoose
# forms.py
from django import forms
from .models import Employee, Payroll, Expense, Income

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'firstName', 'lastName', 'email', 'date_of_birth', 
            'hire_date', 'position', 'salary'
        ]

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee', 'pay_date', 'pay_period_start', 
            'pay_period_end', 'hours_worked', 'gross_pay', 
            'taxes_withheld', 'net_pay'
        ]

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'description', 'amount', 'date'
        ]

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            'source', 'amount', 'date'
        ]
