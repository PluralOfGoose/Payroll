from rest_framework import serializers
from .models import Employee, Payroll, CustomUser

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.
    """
    class Meta:
        model = Employee
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payroll model.
    """
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Payroll
        fields = ['id', 'pay_date', 'pay_period_start', 'pay_period_end', 
                  'hours_worked', 'gross_pay', 'taxes_withheld', 
                  'federal_tax_withheld', 'state_tax_withheld', 
                  'social_security', 'medicare', 'net_pay', 'employee_name']

    def get_employee_name(self, obj):
        # Access the user’s first and last name via the related employee object
        return f"{obj.employee.user.first_name} {obj.employee.user.last_name}"
        # Add or remove fields here as necessary
        # Ensure 'employee' is referenced as a foreign key here if required

class UserSerializer(serializers.ModelSerializer):
  class Meta:
      model = CustomUser
      fields = "__all__"