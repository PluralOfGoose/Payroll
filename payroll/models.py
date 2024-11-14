# Copyright 2024 PluralOfGoose
from django.db import models
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class Employee(models.Model):
    firstName = models.CharField(max_length = 100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    hire_date = models.DateField(default=datetime.now)
    ROLE_CHOICES = {
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    }
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    salary = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        permissions = [
            ("view_own_payroll_info", "Can view own payroll information"),
            ("view_all_payroll_info", "Can view all payroll infomration"),
            ("edit_all_payroll_info", "Can edit all payroll information"),
            ("create_employee_records", "Can create employee records"),
            ("create_payroll_records", "Can create payroll records"),
        ]

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    def can_view_payroll(self, user):
        if user.role == "manager" or user.role == "Manager" or user == self:
            return True
        raise PermissionDenied("You do not have permission to view this payroll information.")
    
    def can_edit_payroll(self, user):
        if user.role == "manager" or user.role == "Manager":
            return True
        raise PermissionDenied("You do not have permission to edit this payroll information.")

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payrolls")
    pay_date = models.DateField()
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    taxes_withheld = models.DecimalField(max_digits=10, decimal_places=2)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payroll for {self.employee} on {self.pay_date}"

    def can_view(self, user):
        if user.role == "manager" or user == self.employee:
            return True
        raise PermissionDenied("You do not have permission to view this payroll information.")

    def can_edit(self, user):
        if user.role == "manager":
            return True
        raise PermissionDenied("You do not have permission to edit this payroll information.")

class Expense(models.Model):
    description = models.CharField(max_length = 225)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField()

    def __str__(self):
        return self.description

class Income(models.Model):
    source = models.CharField(max_length = 225)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField()

    def __str__(self):
        return self.source
    
class CustomUser(AbstractUser, models.Model):
    ROLE_CHOICES = {
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    }
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    #username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    def __str__(self):
        return f"{self.email}"
    



