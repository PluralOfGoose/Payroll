# permissions.py
from rest_framework.permissions import BasePermission
from .models import Employee, Payroll, CustomUser

class IsManager(BasePermission):
    """
    Custom permission to allow only managers to edit or view certain objects.
    """
    def has_permission(self, request, view):
        # Only allow managers to perform actions
        return request.user.role == 'manager'

    def has_object_permission(self, request, view, obj):
        # Managers can view, edit, or delete any object
        return request.user.role == 'manager'


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            print("Authentication failed: User not authenticated")
            return False
        print(f"User authenticated: {request.user}, Role: {request.user.role}")
        return request.user.role == 'employee'

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Payroll):
            return obj.employee.user == request.user
        return False

class IsEmployeeOrManager(BasePermission):
    """
    Custom permission to allow employees to view their own payroll
    and managers to view all payrolls.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Allow if the user is a manager or an employee
        return request.user.role in ['manager', 'employee']

    def has_object_permission(self, request, view, obj):
        # Managers can view any payroll instance
        if request.user.role == 'manager':
            return True

        # Employees can only view their own payroll instance
        if request.user.role == 'employee' and isinstance(obj, Payroll):
            return obj.employee.user == request.user

        return False


class IsManagerForCreatingPayroll(BasePermission):
    """
    Custom permission to allow only managers to create payroll entries.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            print("Authentication failed: User not authenticated")
            return False
        print(f"User authenticated: {request.user}, Role: {request.user.role}")
        return request.user.role == 'manager'

    def has_object_permission(self, request, view, obj):
        # Managers can update any payroll, but employees cannot
        return request.user.role == 'manager'
