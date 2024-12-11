from django.contrib.auth.models import Permission
from django.db.models.signals import post_migrate
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = UserModel
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'last_login', 'user_type')  # 1. Display
    search_fields = ('email', 'username') # 2. Search fields
    ordering = ('username',) # 3. Ordering
    list_filter = ('is_superuser', 'is_staff', 'user_type')  # 4. List filters
    date_hierarchy = 'date_joined'  # 5. Date hierarchy

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type')
        }),
    )

@receiver(post_migrate)
def setup_admin_groups(sender, **kwargs):
    """
    Automatically create Superusers and Staff groups with appropriate permissions after migrations.
    """
    # Define permissions for each group
    superuser_permissions = Permission.objects.all()
    staff_permissions = [
        'view_customuser', 'add_customuser', 'change_customuser',
        'view_property', 'add_property', 'change_property',
        'view_tenant',
        'view_expense', 'add_expense', 'view_income', 'add_income',
    ]

    # Create or update the Superusers group
    superusers_group, created = Group.objects.get_or_create(name="Superusers")
    superusers_group.permissions.set(superuser_permissions)
    print(f"{'Created' if created else 'Updated'} Superusers group with full permissions.")

    # Create or update the Staff group
    staff_group, created = Group.objects.get_or_create(name="Staff")
    staff_group.permissions.clear()
    for codename in staff_permissions:
        try:
            permission = Permission.objects.get(codename=codename)
            staff_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission '{codename}' does not exist. Skipping.")
    print(f"{'Created' if created else 'Updated'} Staff group with limited permissions.")
