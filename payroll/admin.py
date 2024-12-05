from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import CustomUser, Employee, Payroll, Expense, Income

#admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Payroll)
admin.site.register(Expense)
admin.site.register(Income)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Ensure there is no reference to 'usable_password' in these attributes
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Include only valid fields here
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Include only valid fields here
    )
    list_display = ('email', 'username', 'role', 'is_staff')
    search_fields = ('email', 'username')

# Register the admin
admin.site.register(CustomUser, CustomUserAdmin)

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