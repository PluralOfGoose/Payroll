"""
URL configuration for payroll_demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from payroll import views
from payroll.views import EmployeeDetailView, EmployeeListView, PayrollListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from oauth2_provider.views import TokenView, RevokeTokenView
from django.conf.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('employees/', views.employees_list, name='employee_list'),
    path('benefits-overview/', views.benefits_overview, name='benefits_overview'),
    path('summary/', views.payroll_info, name='payroll_summary'),
    path('tax-details/', views.tax_details, name='tax_details'),
    path('add_employee/', views.add_employee, name = 'add_employee'),
    path('add_expense/', views.add_expense, name = 'add_expense'),
    path('add_income/', views.add_income, name = 'add_income'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('payroll/', PayrollListView.as_view(), name='payroll_list'),
    #path('auth/', include('rest_auth.urls')),
]
