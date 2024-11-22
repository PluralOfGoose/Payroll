from django.test import TestCase
from .models import CustomUser
from rest_framework.test import APIClient

class TestIsManagerForCreatingPayroll(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.manager = CustomUser.objects.create_user(email='manager@example.com', role='manager', password='testpass')
        self.employee = CustomUser.objects.create_user(email='employee@example.com', role='employee', password='testpass')

    def test_manager_permission(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/payroll/run/', {})
        self.assertEqual(response.status_code, 200)

    def test_employee_permission(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.post('/payroll/run/', {})
        self.assertEqual(response.status_code, 403)