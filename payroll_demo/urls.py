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
from payroll.views import EmployeeDetailView, EmployeeListView, PayrollListView, CustomLoginView, manager_home, employee_home, profile_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from oauth2_provider.views import TokenView, RevokeTokenView
from django.conf.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('benefits-overview/', views.benefits_overview, name='benefits_overview'),
    path('summary/', views.payroll_info, name='payroll_summary'),
    path('tax-details/', views.tax_details, name='tax_details'),
    path('add_employee/', views.add_employee, name = 'add_employee'),
    path('add_expense/', views.add_expense, name = 'add_expense'),
    path('add_income/', views.add_income, name = 'add_income'),
]

urlpatterns += [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('manager/home/', views.manager_home, name='manager_home'),
    path('employee/home/', views.employee_home, name='employee_home'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('employees/', views.employee_list, name='employee_list'),
    path('add_employee/', views.add_employee, name='add_employee1'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/run/', views.run_payroll, name='run_payroll'),
    path('employee/tax-documents/', views.tax_documents, name='tax_documents'),
    path('create-user-ajax/', views.create_user_ajax, name='create_user_ajax'),
    path('edit_employee/', views.edit_employee, name='edit_employee'),
    #path('auth/', include('rest_auth.urls')),
]
