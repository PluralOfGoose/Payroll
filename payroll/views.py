# views.py
# Copyright 2024 dhannon

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from .forms import EmployeeForm, ExpenseForm, IncomeForm, CustomUserCreationForm
from .models import Employee, Payroll, Expense, Income, CustomUser
from rest_framework import status, permissions, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmployeeSerializer, PayrollSerializer
from .permissions import IsManager, IsEmployee
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'payroll/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'manager':
            return reverse_lazy('manager_home')  # Redirect to manager's home page
        else:
            return reverse_lazy('employee_home')  # Redirect to employee's home page


@login_required
def manager_home(request):
    # Ensure only managers can access
    if request.user.role != 'manager':
        return redirect('employee_home')
    employees = Employee.objects.all()
    payrolls = Payroll.objects.all()
    # Add additional context as needed for the manager's dashboard
    return render(request, 'payroll/manager_home.html', {'employees': employees, 'payrolls': payrolls})


@login_required
def employee_home(request):
    # Ensure only employees can access
    if request.user.role == 'employee':
        payrolls = Payroll.objects.filter(employee__user=request.user)
        # Additional context for the employee dashboard
        return render(request, 'payroll/employee_home.html', {'payrolls': payrolls})
    else:
        return redirect('manager_home')
    
@login_required
def profile_view(request):
    return render(request, 'payroll/profile.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    employees = Employee.objects.all()
    payrolls = Payroll.objects.all()
    return render(request, 'payroll/home.html', {'employees': employees, 'payrolls': payrolls})


@login_required
def employee_list(request):
    # Retrieve all employees
    employees = Employee.objects.all()

    # Pass the employee list to the template
    return render(request, 'payroll/employee_list.html', {'employees': employees})


def payroll_info(request):
    payrolls = Payroll.objects.all()
    return render(request, 'payroll_info.html', {'payrolls': payrolls})


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()
    return render(request, 'payroll/add_employee.html', {'form': form})


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'payroll/add_expense.html', {'form': form})


def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'payroll/add_income.html', {'form': form})


def tax_details(request):
    return render(request, 'payroll/tax_details.html')


def benefits_overview(request):
    return render(request, 'payroll/benefits_overview.html')

def employee_list(request):
    return render(request, 'payroll/employee_list.html')

class EmployeeListView(ListView):
    model = Employee
    template_name = 'payroll/employee_list.html'
    context_object_name = 'employees'
    permission_classes = [IsManager]


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsManager]


class PayrollListView(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = PayrollSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        # Filter payroll records based on the user's role
        user = self.request.user
        if user.role == 'manager':
            return Payroll.objects.all()  # Managers can view all payrolls
        else:
            return Payroll.objects.filter(employee__user=user)  # Employees can view only their payrolls
