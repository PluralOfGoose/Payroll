# Copyright 2024 dhannon
from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(models.Model):
    firstName = models.CharField(max_length = 100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    date_of_birth = models.DateField()
    hire_date = models.DateField()
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
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
    
class customuser(AbstractUser):
    ROLE_CHOICES = {
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    }
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    email = models.EmailField(max_length=100)


