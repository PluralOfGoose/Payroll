# Copyright 2024 dhannon
from django.shortcuts import render, redirect
from .forms import EmployeeForm, ExpenseForm, IncomeForm
from .models import Employee, Payroll, Expense, Income
from rest_framework import status, permissions, viewsets
from rest_framework import response
from rest_framework import generics
from .serializers import EmployeeSerializer, PayrollSerializer
from .permissions import IsManager, IsEmployee
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView


def home(request):
    #total_expenses = sum(exp.amount for exp in Expense.objects.all())
    #total_income = sum(inc.amount for inc in Income.objects.all())
    #profit = total_income - total_expenses
    employees = Employee.objects.all()
    payrolls = Payroll.objects.all()

    return render(request, 'payroll/home.html', {'employees': employees, 'payrolls': payrolls})#, 'total_income': total_income})

def employees_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def payroll_info(request):
    payrolls = Payroll.objects.all()
    return render(request, 'payroll_info.html', {'payrolls': payrolls})

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

def tax_details(request):
    # Logic to fetch and display tax details data
    return render(request, 'payroll/tax_details.html')

def benefits_overview(request):
    # Logic to display benefits overview data
    return render(request, 'payroll/benefits_overview.html')

class EmployeeListView(ListView):
    model = Employee
    template_name = 'payroll/employee_list.html'
    context_object_name = 'employees'
    permission_classes = [IsManager]

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsManager]

class PayrollListView(generics.ListAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        # Only show payroll information for the current user (employee)
        return Payroll.objects.filter(employee=self.request.user)