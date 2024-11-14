# Generated by Django 5.1.2 on 2024-11-13 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'permissions': [('view_own_payroll_info', 'Can view own payroll information'), ('view_all_payroll_info', 'Can view all payroll infomration'), ('edit_all_payroll_info', 'Can edit all payroll information'), ('create_employee_records', 'Can create employee records'), ('create_payroll_records', 'Can create payroll records')]},
        ),
        migrations.RemoveField(
            model_name='employee',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='position',
        ),
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('employee', 'Employee'), ('manager', 'Manager')], default='employee', max_length=10),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('employee', 'Employee'), ('manager', 'Manager')], default='employee', max_length=10),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
