from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model
from .models import SupplierProduct,ManufacturerProduct
class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2','role')
    # def __init__(self, *args, **kwargs):
    #     super(CreateUserForm, self).__init__(*args, **kwargs)

    #     self.fields['first_name'].widget.attrs['class'] = 'form-control'
    #     self.fields['username'].widget.attrs['class'] = 'form-control'
    #     self.fields['email'].widget.attrs['class'] = 'form-control'
    #     self.fields['role'].widget.attrs['class'] = 'form-control'
    #     self.fields['password1'].widget.attrs['class'] = 'form-control'
    #     self.fields['password2'].widget.attrs['class'] = 'form-control'

        # for fieldname in ['username', 'password1', 'password2']:
        #     self.fields[fieldname].help_text = None

class SupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        fields = ['name', 'price', 'quality','credit_period', 'quantity', 'type', 'is_available']
        labels = {
            'name': 'Name',
            'price': 'Price',
            'quality': 'Quality',
            'quantity': 'Quantity',
            'type': 'Type',
            'is_available': 'Is Available',
            'credit_period':'credit_period'
        }

class ManufacturerProductForm(forms.ModelForm):
    class Meta:
        model = ManufacturerProduct
        fields = ['name', 'price', 'quality', 'quantity', 'type', 'is_available','credit_period']
        labels = {
            'name': 'Name',
            'price': 'Price',
            'quality': 'Quality',
            'quantity': 'Quantity',
            'type': 'Type',
            'is_available': 'Is Available',
            'credit_period':'credit_period'
        }

