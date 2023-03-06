from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, SupplierProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticateduser,allowed_users
from django.contrib.auth.models import Group
from .models import SupplierDetails,SupplierProduct
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from itertools import chain
# Create your views here.

@unauthenticateduser
def index(request):
    return render(request, 'index.html')

@unauthenticateduser
def rolls(request):
    return render(request, 'rolls.html')





# Supplier

@allowed_users(allowed_roles=['SUPPLIER'])
def supplier_home(request):
    user_products = SupplierProduct.objects.filter(user=request.user).order_by('type')
    type_list = sorted(set([p.type for p in user_products]))
    # Combine products with the same type into a single list
    user_products = list(chain.from_iterable([list(filter(lambda p: p.type == t, user_products)) for t in type_list]))
    context = {'user_products': user_products}
    return render(request, 'supplier_home.html',context)

@allowed_users(allowed_roles=['SUPPLIER'])
def supplier_profile(request):
    #To check if supplier details already exist
    user_details = 'disp_mode'
    try:
        supplier_profile = SupplierDetails.objects.get(user=request.user)
        address = supplier_profile.address
        contact_person = supplier_profile.contact_person
        phone_number = supplier_profile.phone_number
        gst_number = supplier_profile.gst_number
        if request.method == 'POST':
            if 'edit' in request.POST:
                user_details = 'edit_mode'
            elif 'submit' in request.POST:
                supplier_profile.address = request.POST['address']
                supplier_profile.contact_person = request.POST['contact_person']
                supplier_profile.phone_number = request.POST['phone_number']
                supplier_profile.gst_number = request.POST['gst_number']
                supplier_profile.save()
                address = supplier_profile.address
                contact_person = supplier_profile.contact_person
                phone_number = supplier_profile.phone_number
                gst_number = supplier_profile.gst_number                
                messages.success(request, 'Profile updated successfully!')
                user_details = 'disp_mode'
    except SupplierDetails.DoesNotExist:
        if request.method == 'POST':
            if 'submit' in request.POST:
                address = request.POST['address']
                contact_person = request.POST['contact_person']
                phone_number = request.POST['phone_number']
                gst_number = request.POST['gst_number']
                supplier_profile = SupplierDetails(user=request.user,
                                                   address= address,
                                                   contact_person= contact_person,
                                                   phone_number= phone_number,
                                                   gst_number= gst_number)
                supplier_profile.save()
                messages.success(request, 'Profile created successfully!')
                user_details = 'disp_mode'
        else:
            user_details = 'edit_mode'
            address = ''
            contact_person = ''
            phone_number = ''
            gst_number = ''
    context = {
        'user_details': user_details,
        'address': address,
        'contact_person': contact_person,
        'phone_number': phone_number,
        'gst_number': gst_number,
    }
    return render(request, 'supplier_profile.html', context)


@allowed_users(allowed_roles=['SUPPLIER'])
def add_product_supplier(request):
    if request.method == 'POST':
        form = SupplierProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('supplier_home')
    else:
        form = SupplierProductForm()
    return render(request, 'add_product_supplier.html', {'form': form})


# Manufacturer

@allowed_users(allowed_roles=['MANUFACTURER'])
def manufacturer_home(request):
    return render(request, 'manufacturer_home.html')

# Retailer

@allowed_users(allowed_roles=['RETAILER'])
def retailer_home(request):
    return render(request, 'retailer_home.html')

# Admin items


@login_required(login_url='user_login') #put admin_login for admin
def admin_home(request):
    return render(request, 'admin.html')

@unauthenticateduser
def user_signup(request):
    form = CreateUserForm()
    print(request.POST)
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            role = form.cleaned_data.get('role')
            print("role",role)
            group = Group.objects.get(name=role)
            user.groups.add(group)
            return redirect('user_login')
        else:
            print(form.errors)
            print("ERROR not valid form")
    else:
        print("ERROR")
    context = {'form': form}
    return render(request, 'user_signup', context)


@unauthenticateduser
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(email)
        # print(password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # print(user)
            role = str(request.user.groups.all()[0])
            if role == 'SUPPLIER':
                dynamic_login_url = 'supplier_home'
            elif role == 'MANUFACTURER':
                dynamic_login_url = 'manufacturer_home'
            else:
                dynamic_login_url = 'retailer_home'
            return redirect(dynamic_login_url)
            # return redirect('admin_home')
        else:
            # print(user)
            print("error in user match")
    else:
        print("ERROR in post method")

    context = {}
    return render(request, 'user_login.html',context)

def user_logout(request):
    logout(request)
    return redirect('user_login')