from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticateduser
# Create your views here.


def index(request):
    return render(request, 'index.html')


def rolls(request):
    return render(request, 'rolls.html')

# Supplier


def supplier_home(request):
    return render(request, 'supplier_home.html')

# Manufacturer


def manufacturer_home(request):
    return render(request, 'manufacturer_home.html')

# Retailer


def retailer_home(request):
    return render(request, 'retailer_home.html')

# Admin items


@login_required(login_url='admin_login')
def admin_home(request):
    return render(request, 'admin.html')

@unauthenticateduser
def admin_signup(request):
    form = CreateUserForm()
    print(request.POST)
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_login')
        else:
            print(form.errors)
            print("ERROR not valid form")
    else:
        print("ERROR")
    context = {'form': form}
    return render(request, 'admin_signup', context)


@unauthenticateduser
def admin_login(request):
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
            return redirect('admin_home')
        else:
            # print(user)
            print("error in user match")
    else:
        print("ERROR in post method")

    context = {}
    return render(request, 'admin_login.html',context)

def admin_logout(request):
    logout(request)
    return redirect('admin_login')