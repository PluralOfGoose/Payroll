# Copyright 2024 dhannon
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length = 100)
    salary = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.name

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

