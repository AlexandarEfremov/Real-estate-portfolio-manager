from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

UserModel = get_user_model()

@admin.register(UserModel)
class UserAdmin(DefaultUserAdmin):
    # Display useful user fields in the admin list view
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Fieldsets for the user detail view in the admin
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to display when creating a new user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.unregister(Group)


class StaffGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def save_model(self, request, obj, form, change):
        """Ensure staff group gets appropriate permissions on creation."""
        super().save_model(request, obj, form, change)
        if obj.name == "Staff":
            # Assign limited permissions to the "Staff" group
            content_types = ContentType.objects.filter(app_label__in=['finance', 'tenants', 'properties'])
            limited_permissions = Permission.objects.filter(content_type__in=content_types).exclude(codename__icontains='delete')
            obj.permissions.set(limited_permissions)

admin.site.register(Group, StaffGroupAdmin)
