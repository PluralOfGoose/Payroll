from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Employee, Payroll, Expense, Income

admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Payroll)
admin.site.register(Expense)
admin.site.register(Income)

'''@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Customize how the user is displayed in the admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add any custom fields here
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Add any custom fields here
    )

    list_display = ['email', 'username', 'first_name', 'last_name', 'role']
'''