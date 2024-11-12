from rest_framework import serializers
from .models import Employee, Payroll

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
    class Meta:
        model = Payroll
        fields = '__all__'
        # Add or remove fields here as necessary
        # Ensure 'employee' is referenced as a foreign key here if required
