# views.py
# Copyright 2024 dhannon

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from datetime import date
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.core.exceptions import PermissionDenied
from .forms import EmployeeCreationForm, ExpenseForm, IncomeForm, CustomUserCreationForm, PayrollForm
from .models import Employee, Payroll, Expense, Income, CustomUser
from rest_framework import status, permissions, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmployeeSerializer, PayrollSerializer
from .permissions import IsManager, IsEmployee
from django.contrib.auth.views import LoginView
from .utils import get_state_tax_rate, calculate_payroll


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


from django.utils.timezone import now
from django.db.models import Sum

@login_required
def employee_home(request):
    if request.user.role != 'employee':
        return redirect('manager_home')

    # Get the current employee
    try:
        employee = request.user.employee_profile  # Assuming OneToOne relationship with Employee
    except Employee.DoesNotExist:
        return redirect('login')  # Redirect if the employee profile is not set up

    # Total amount paid this year
    current_year = now().year
    total_paid = Payroll.objects.filter(
        employee=employee,
        pay_date__year=current_year
    ).aggregate(total=Sum('net_pay'))['total'] or 0.00

    # Get the next pay period
    next_payroll = Payroll.objects.filter(
        employee=employee,
        pay_date__gt=now()
    ).order_by('pay_date').first()

    next_pay_period_start = next_payroll.pay_period_start if next_payroll else "N/A"
    next_pay_period_end = next_payroll.pay_period_end if next_payroll else "N/A"

    context = {
        'total_paid': total_paid,
        'next_pay_period_start': next_pay_period_start,
        'next_pay_period_end': next_pay_period_end,
    }
    return render(request, 'payroll/employee_home.html', context)

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
    if request.user.role != 'manager':
        raise PermissionDenied("Only managers can add employees.")

    if request.method == 'POST':
        if 'user_form' in request.POST:
            # Handle user creation form submission
            user_form = CustomUserCreationForm(request.POST)
            employee_form = EmployeeCreationForm()  # Create an empty employee form
            if user_form.is_valid():
                user = user_form.save()
                return JsonResponse({'success': True, 'user_id': user.id, 'username': user.username})
            else:
                return JsonResponse({'success': False, 'error': user_form.errors.as_json()}, status=400)

        elif 'employee_form' in request.POST:
            # Handle employee creation form submission
            employee_form = EmployeeCreationForm(request.POST)
            user_form = CustomUserCreationForm()  # Create an empty user form
            if employee_form.is_valid():
                employee_form.save()
                return redirect('employee_list')  # Redirect to the employee list after saving
    else:
        # Initialize both forms for GET request
        user_form = CustomUserCreationForm()
        employee_form = EmployeeCreationForm()

    return render(request, 'payroll/add_employee.html', {'user_form': user_form, 'employee_form': employee_form})

@csrf_exempt
def create_user_ajax(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            return JsonResponse({
                'success': True,
                'user_id': user.id,
                'username': user.username
            })
        else:
            return JsonResponse({
                'success': False,
                'error': user_form.errors.as_json()},
                 status=400
            )

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
    if request.user.role != 'manager':  # Additional check
        raise PermissionDenied("Only managers can view this page.")
    
    employees = Employee.objects.all()  # Fetch all employees
    return render(request, 'payroll/employee_list.html', {'employees': employees})

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
        
from .utils import calculate_payroll

@login_required
def run_payroll(request):
    if request.user.role != 'manager':  # Ensure user is a manager
        raise PermissionDenied("Only managers can run payroll.")

    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save(commit=False)

            state = form.cleaned_data['state']

            # Get data from form or POST request
            employee = payroll.employee
            hours_worked = payroll.hours_worked
            hourly_rate = payroll.employee.salary / 2080  # Assuming 2080 work hours/year
            
            # Use the `calculate_payroll` function to compute payroll
            payroll_data = calculate_payroll(hours_worked, hourly_rate, state)

            # Save calculated payroll details to the payroll object
            payroll.gross_pay = payroll_data['gross_pay']
            payroll.taxes_withheld = payroll_data['taxes_withheld']
            payroll.net_pay = payroll_data['net_pay']
            payroll.pay_date = date.today()  # Default pay date to today
            
            payroll.pay_period_start = form.cleaned_data['pay_period_start']
            payroll.pay_period_end = form.cleaned_data['pay_period_end']
            
            payroll.save()

            return redirect('payroll_list')  # Redirect to payroll list page after saving
    else:
        form = PayrollForm()

    employees = Employee.objects.all()  # Fetch all employees
    return render(request, 'payroll/run_payroll.html', {'form': form, 'employees': employees})

@login_required
def tax_documents(request):
    if request.user.role != 'employee':
        raise PermissionDenied("Only employees can access this page.")

    # Logic to fetch tax documents, e.g., from a database or storage
    tax_documents = []  # Replace with actual logic to retrieve tax documents

    return render(request, 'payroll/tax_documents.html', {'tax_documents': tax_documents})