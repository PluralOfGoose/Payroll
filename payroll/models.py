# models.py

from django.db import models
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class CustomUser(AbstractUser):
    ROLE_CHOICES = {
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    }
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employee_profile")
    hire_date = models.DateField(default=datetime.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # New field to track yearly total

    class Meta:
        permissions = [
            ("view_own_payroll_info", "Can view own payroll information"),
            ("view_all_payroll_info", "Can view all payroll information"),
            ("edit_all_payroll_info", "Can edit all payroll information"),
            ("create_employee_records", "Can create employee records"),
            ("create_payroll_records", "Can create payroll records"),
        ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def can_view_payroll(self, user):
        if user.role == "manager" or user == self.user:
            return True
        raise PermissionDenied("You do not have permission to view this payroll information.")

    def can_edit_payroll(self, user):
        if user.role == "manager":
            return True
        raise PermissionDenied("You do not have permission to edit this payroll information.")

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payrolls")
    pay_date = models.DateField()
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    taxes_withheld = models.DecimalField(max_digits=10, decimal_places=2)  # Legacy field for total taxes
    federal_tax_withheld = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    state_tax_withheld = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    social_security = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medicare = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payroll for {self.employee.user.get_full_name()} on {self.pay_date}"


    def can_view(self, user):
        if user.role == "manager" or user == self.employee.user:
            return True
        raise PermissionDenied("You do not have permission to view this payroll information.")

    def can_edit(self, user):
        if user.role == "manager":
            return True
        raise PermissionDenied("You do not have permission to edit this payroll information.")

class Expense(models.Model):
    description = models.CharField(max_length=225)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.description

class Income(models.Model):
    source = models.CharField(max_length=225)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.source
    
class W2(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.IntegerField()
    wages = models.DecimalField(max_digits=10, decimal_places=2)
    federal_tax_withheld = models.DecimalField(max_digits=10, decimal_places=2)
    state_tax_withheld = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    social_security_wages = models.DecimalField(max_digits=10, decimal_places=2)
    medicare_wages = models.DecimalField(max_digits=10, decimal_places=2)
    employer_name = models.CharField(max_length=255)
    employer_ein = models.CharField(max_length=9)  # Employer Identification Number
    employer_address = models.TextField()

    def __str__(self):
        return f"W-2 for {self.employee} ({self.year})"