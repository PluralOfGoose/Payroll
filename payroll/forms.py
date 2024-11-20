# forms.py
# Copyright 2024 dhannon & PluralofGoose

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from .models import Employee, Payroll, Expense, Income, CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user with additional fields."""
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'role']  # Fields for registration form
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class EmployeeCreationForm(forms.ModelForm):
    """Form for creating user"""
    class Meta:
        model = Employee
        fields = ['user', 'salary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(employee_profile__isnull=True)

class EmployeeForm(forms.ModelForm):
    """Form for creating or updating employee records."""
    class Meta:
        model = Employee
        fields = ['user', 'hire_date', 'salary']  # Use 'user' to link to CustomUser, and other Employee-specific fields

class PayrollForm(forms.ModelForm):
    """Form for creating or updating payroll records."""
    state = forms.ChoiceField(choices=[
        ('NY', 'New York'),
        ('CA', 'California'),
        ('TX', 'Texas'),
        # Add more states as needed
    ], required=True)

    class Meta:
        model = Payroll
        fields = [
            'employee', 'hours_worked', 'pay_period_start', 'pay_period_end'
        ]

        widgets = {
            'pay_period_start': forms.DateInput(attrs={'type': 'date'}),
            'pay_period_end': forms.DateInput(attrs={'type': 'date'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['employee'].widget = Select(
                choices=[
                    (e.id, mark_safe(f'{e.user.first_name} {e.user.last_name} (Rate: ${e.salary / 2080:.2f})'))
                    for e in Employee.objects.all()
                ],
                attrs={
                    'data-hourly-rate': lambda employee: employee.salary / 2080 
                }
            )

        def clean(self):
            cleaned_data = super().clean()
            pay_period_start = cleaned_data.get('pay_period_start')
            pay_period_end = cleaned_data.get('pay_period_end')

            if pay_period_start and pay_period_end:
                if pay_period_start > pay_period_end:
                    raise ValidationError("Pay period start date mest be before pay period end date")

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
