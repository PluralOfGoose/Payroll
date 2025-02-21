# views.py
# Copyright 2024 dhannon

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from datetime import date
from django.utils.timezone import now
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .utils import generate_pdf, calculate_payroll
from django.core.exceptions import PermissionDenied
from . import models
from .forms import EmployeeCreationForm, ExpenseForm, IncomeForm, CustomUserCreationForm, PayrollForm, EditEmployeeForm
from .models import Employee, Payroll, Expense, Income, CustomUser, W2
from rest_framework import status, permissions, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .serializers import EmployeeSerializer, PayrollSerializer
from .permissions import IsManager, IsEmployeeOrManager, IsEmployee
from django.contrib.auth.views import LoginView
from .utils import get_state_tax_rate, calculate_payroll
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO


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

@login_required
def edit_employee(request):
    if request.user.role != 'manager':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('manager_home')

    if request.method == 'POST':
        form = EditEmployeeForm(request.POST)
        if form.is_valid():
            # Retrieve the selected employee
            employee = form.cleaned_data['employee']

            # Update fields only if provided
            if form.cleaned_data['first_name']:
                employee.user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name']:
                employee.user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['email']:
                employee.user.email = form.cleaned_data['email']
            if form.cleaned_data['salary']:
                employee.salary = form.cleaned_data['salary']

            # Save changes
            employee.user.save()
            employee.save()

            messages.success(request, "Employee information updated successfully.")
            return redirect('edit_employee')
    else:
        form = EditEmployeeForm()

    # Fetch all employees for the dropdown
    employees = Employee.objects.all()
    return render(request, 'payroll/edit_employee.html', {'form': form, 'employees': employees})

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


class PayrollListView(generics.ListAPIView):
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated, IsEmployeeOrManager]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            # Managers can view all payrolls
            return Payroll.objects.all()
        else:
            # Employees can only view their own payrolls
            return Payroll.objects.filter(employee__user=user)
        
@login_required
def payroll_list(request):
    user = request.user

    # Fetch payroll data based on the user's role
    if user.role == 'manager':
        payrolls = Payroll.objects.all()  # Managers see all payrolls
    else:
        payrolls = Payroll.objects.filter(employee__user=user)  # Employees see their own payrolls

    # Pass payroll data to the template
    context = {
        'payrolls': payrolls,
    }
    return render(request, 'payroll/payroll_list.html', context)

from .utils import calculate_payroll

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO

@login_required
def run_payroll(request):
    if request.user.role != 'manager':  # Ensure user is a manager
        raise PermissionDenied("Only managers can run payroll.")

    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save(commit=False)

            # Extract data from the form
            state = form.cleaned_data['state']
            employee = payroll.employee
            hours_worked = payroll.hours_worked
            hourly_rate = employee.salary / 2080  # Calculate hourly rate

            # Use the calculate_payroll function
            payroll_data = calculate_payroll(hours_worked, hourly_rate, state)

            # Assign calculated values to payroll instance
            payroll.gross_pay = payroll_data['gross_pay']
            payroll.state_tax_withheld = payroll_data['state_taxes_withheld']
            payroll.medicare = payroll_data['medicare_taxes']
            payroll.social_security = payroll_data['social_security_taxes']
            payroll.net_pay = payroll_data['net_pay']
            payroll.taxes_withheld = payroll_data['taxes_withheld']

            # Save the payroll instance
            payroll.pay_period_start = form.cleaned_data['pay_period_start']
            payroll.pay_period_end = form.cleaned_data['pay_period_end']
            payroll.pay_date = date.today()  # Default to today
            payroll.save()

            # Update the employee's total earnings
            employee.total += payroll.gross_pay
            employee.save()

            return redirect('payroll_list')  # Redirect to payroll list page

    else:
        form = PayrollForm()

    employees = Employee.objects.all()
    return render(request, 'payroll/run_payroll.html', {'form': form, 'employees': employees})

def event_listen(request):
    return render(request, 'payroll/event_listener.html')

def read_me(request):
    return render(request, 'payroll/read_me.html')

@login_required
def tax_documents(request):
    if request.user.role != 'employee':
        raise PermissionDenied("Only employees can access this page.")

    # Logic to fetch tax documents, e.g., from a database or storage
    tax_documents = []  # Replace with actual logic to retrieve tax documents

    return render(request, 'payroll/tax_documents.html', {'tax_documents': tax_documents})

@login_required
def generate_w2(request):
    # Ensure only managers can access
    if request.user.role != 'manager':
        return HttpResponse("Unauthorized", status=403)

    year = request.GET.get('year', None)
    employee_id = request.GET.get('employee_id', None)

    # Fetch employees and filter Payroll records
    employees = Employee.objects.all()
    payrolls = Payroll.objects.filter(pay_date__year=year, employee_id=employee_id) if year and employee_id else []

    if request.method == 'POST' and year and employee_id:
        # Aggregate W-2 data
        total_earnings = sum(payroll.gross_pay for payroll in payrolls)
        #total_federal_tax = payrolls.aggregate(total=models.Sum('state_tax_withheld'))['total'] or 15
        total_state_tax = payrolls.aggregate(total=Sum('state_tax_withheld'))['total'] or 15
        total_social_security = payrolls.aggregate(total=Sum('social_security'))['total'] or 18
        total_medicare = payrolls.aggregate(total=Sum('medicare'))['total'] or 20

        # Get employee
        employee = Employee.objects.get(pk=employee_id)

        # Render W-2 template
        context = {
            'employee': employee,
            'year': year,
            'total_earnings': total_earnings,
            #'federal_tax': total_federal_tax,
            'state_tax': total_state_tax,
            'social_security': total_social_security,
            'medicare': total_medicare,
        }
        html = render_to_string('payroll/w2_template.html', context)

        # Generate PDF
        pdf = generate_pdf('payroll/w2_template.html', context)

        # Return PDF response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="W2_{employee.user.get_full_name()}_{year}.pdf"'
        return response

    context = {
        'employees': employees,
        'payrolls': payrolls,
        'year': year,
        'selected_employee': employee_id,
    }
    return render(request, 'payroll/generate_w2.html', context)

from rest_framework.permissions import AllowAny

class PayrollListAPI(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Payroll.objects.all()  # List all payroll records
    serializer_class = PayrollSerializer  # Use the PayrollSerializer for serialization

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data.get('amount')  # Amount in cents
            currency = 'usd'  # Default currency
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata={'integration_check': 'accept_a_payment'}
            )
            return JsonResponse({'clientSecret': intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@csrf_exempt
def stripe_payment_view(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Create a PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=5000,  # Amount in cents ($50.00)
        currency='usd',
        payment_method_types=['card'],
    )

    return render(request, 'payroll/stripe_payment.html', {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    })
    
    #return redirect('home')

from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomUserRegistrationForm
#from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of the page to redirect to after registration
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'payroll/register.html', {'form': form})