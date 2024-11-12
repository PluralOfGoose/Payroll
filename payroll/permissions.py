# permissions.py
from rest_framework.permissions import BasePermission
from .models import Employee, Payroll

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
    """
    Custom permission to allow employees to view only their own payroll information.
    """
    def has_permission(self, request, view):
        # Allow employees to view their own data
        return request.user.role == 'employee'

    def has_object_permission(self, request, view, obj):
        # Employees can only view their own payroll information
        if isinstance(obj, Payroll):
            return obj.employee == request.user
        return False  # No access for non-payroll objects or if conditions are not met


class IsEmployeeOrManager(BasePermission):
    """
    Custom permission to allow managers and employees to view employee details.
    """
    def has_permission(self, request, view):
        # Allow both managers and employees to access employee data
        return request.user.role in ['manager', 'employee']

    def has_object_permission(self, request, view, obj):
        # Employees can view only their own details, managers can view all details
        if isinstance(obj, Employee):
            return obj == request.user or request.user.role == 'manager'
        return False


class IsManagerForCreatingPayroll(BasePermission):
    """
    Custom permission to allow only managers to create payroll entries.
    """
    def has_permission(self, request, view):
        # Only managers can create payroll entries
        return request.user.role == 'manager'

    def has_object_permission(self, request, view, obj):
        # Managers can update any payroll, but employees cannot
        return request.user.role == 'manager'
