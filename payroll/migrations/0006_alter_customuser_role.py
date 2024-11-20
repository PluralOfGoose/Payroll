# Generated by Django 5.1.2 on 2024-11-19 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_remove_employee_email_remove_employee_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('employee', 'Employee'), ('manager', 'Manager')], default='employee', max_length=10),
        ),
    ]
