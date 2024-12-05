# Generated by Django 5.1.2 on 2024-12-04 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0004_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('manager', 'Manager'), ('employee', 'Employee')], default='employee', max_length=10),
        ),
        migrations.CreateModel(
            name='W2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('wages', models.DecimalField(decimal_places=2, max_digits=10)),
                ('federal_tax_withheld', models.DecimalField(decimal_places=2, max_digits=10)),
                ('state_tax_withheld', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('social_security_wages', models.DecimalField(decimal_places=2, max_digits=10)),
                ('medicare_wages', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employer_name', models.CharField(max_length=255)),
                ('employer_ein', models.CharField(max_length=9)),
                ('employer_address', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.employee')),
            ],
        ),
    ]
