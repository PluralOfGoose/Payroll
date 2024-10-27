# Copyright 2024 dhannon
from django.shortcuts import render, redirect
from .forms import EmployeeForm, ExpenseForm, IncomeForm
from .models import Employee, Expense, Income

def home(request):
    total_expenses = sum(exp.amount for exp in Expense.objects.all())
    total_income = sum(inc.amount for inc in Income.objects.all())
    profit = total_income - total_expenses
    return render(request, 'payroll/home.html', {'profit': profit, 'total_expenses': total_expenses, 'total_income': total_income})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # Redirect to home page after saving
    else:
        form = EmployeeForm()
    return render(request, 'payroll/add_employee.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # Redirect to home page after saving
    else:
        form = ExpenseForm()
    return render(request, 'payroll/add_expense.html', {'form': form})

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # Redirect to home page after saving
    else:
        form = IncomeForm()
    return render(request, 'payroll/add_income.html', {'form': form})
