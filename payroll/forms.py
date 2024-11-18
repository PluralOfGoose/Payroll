# forms.py
# Copyright 2024 dhannon & PluralofGoose

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Payroll, Expense, Income, CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user with additional fields."""
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'role']  # Fields for registration form

class EmployeeForm(forms.ModelForm):
    """Form for creating or updating employee records."""
    class Meta:
        model = Employee
        fields = ['user', 'hire_date', 'salary']  # Use 'user' to link to CustomUser, and other Employee-specific fields

class PayrollForm(forms.ModelForm):
    """Form for creating or updating payroll records."""
    class Meta:
        model = Payroll
        fields = [
            'employee', 'pay_date', 'pay_period_start', 
            'pay_period_end', 'hours_worked', 'gross_pay', 
            'taxes_withheld', 'net_pay'
        ]

class ExpenseForm(forms.ModelForm):
    """Form for creating or updating expense records."""
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date']

class IncomeForm(forms.ModelForm):
    """Form for creating or updating income records."""
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']
