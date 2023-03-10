from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,SupplierDetails,SupplierProduct

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_superuser', 'groups')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password', 'is_staff', 'is_superuser', 'groups')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_superuser', 'groups'),
        }),
    )
admin.site.register(User, CustomUserAdmin)

#class for Supplier Details
class SupplierDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'contact_person', 'quality_score', 'gst_number','address','status')
    search_fields = ('user__username', 'user__email', 'contact_person', 'gst_number','address')

admin.site.register(SupplierDetails, SupplierDetailsAdmin)


class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quality', 'quantity', 'type', 'is_available')

admin.site.register(SupplierProduct,SupplierProductAdmin)

