from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticateduser,allowed_users
from django.contrib.auth.models import Group
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
    return render(request, 'supplier_home.html')

@allowed_users(allowed_roles=['SUPPLIER'])
def supplier_profile(request):
    return render(request, 'supplier_profile.html')

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