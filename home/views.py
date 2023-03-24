from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, SupplierProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticateduser,allowed_users
from django.contrib.auth.models import Group
from .models import SupplierDetails,SupplierProduct,User,SupplierOrder
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from itertools import chain
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime

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
def edit_product_supplier(request, product_id):
    product = get_object_or_404(SupplierProduct, id=product_id)
    if request.method == 'GET':
        context = {
            'product': product
        }
        return render(request, 'edit_product_supplier.html', context)
    elif request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.quality = request.POST.get('quality')
        product.quantity = request.POST.get('quantity')
        product.type = request.POST.get('type')
        product.is_available = request.POST.get('is_available', False) == 'on'
        product.save()
        return redirect('supplier_home')

@allowed_users(allowed_roles=['SUPPLIER'])
def delete_product_supplier(request, product_id):
    product = SupplierProduct.objects.get(id=product_id)
    product.delete()
    return redirect('supplier_home')

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
        status = supplier_profile.status
        print(status)
        profile_picture = supplier_profile.profile_pic.url if supplier_profile.profile_pic else None
        if request.method == 'POST':
            if 'edit' in request.POST:
                user_details = 'edit_mode'
            elif 'submit' in request.POST:
                supplier_profile.address = request.POST['address']
                supplier_profile.contact_person = request.POST['contact_person']
                supplier_profile.phone_number = request.POST['phone_number']
                supplier_profile.gst_number = request.POST['gst_number']
                supplier_profile.status = 'Pending' # give P in caps or will get error
                print(supplier_profile.status)
                # Get and validate the profile picture
                profile_picture = request.FILES.get('profile_picture')
                print(profile_picture)
                if profile_picture:
                    supplier_profile.profile_pic = profile_picture
                supplier_profile.save()
                print(supplier_profile.status)
                address = supplier_profile.address
                contact_person = supplier_profile.contact_person
                phone_number = supplier_profile.phone_number
                gst_number = supplier_profile.gst_number
                status = supplier_profile.status                
                profile_picture = supplier_profile.profile_pic.url if supplier_profile.profile_pic else None
                messages.success(request, 'Profile updated successfully!')
                user_details = 'disp_mode'
    except SupplierDetails.DoesNotExist:
        if request.method == 'POST':
            if 'submit' in request.POST:
                address = request.POST['address']
                contact_person = request.POST['contact_person']
                phone_number = request.POST['phone_number']
                gst_number = request.POST['gst_number']
                # Get and validate the profile picture
                profile_picture = request.FILES.get('profile_picture')
                supplier_profile = SupplierDetails(user=request.user,
                                                   address= address,
                                                   contact_person= contact_person,
                                                   phone_number= phone_number,
                                                   gst_number= gst_number,
                                                   status='Pending')
                if profile_picture:
                    supplier_profile.profile_pic = profile_picture
                supplier_profile.save()
                messages.success(request, 'Profile created successfully!')
                user_details = 'disp_mode'
        else:
            user_details = 'edit_mode'
            address = ''
            contact_person = ''
            phone_number = ''
            gst_number = ''
            status = 'Pending'
            profile_picture = None
    context = {
        'user_details': user_details,
        'address': address,
        'contact_person': contact_person,
        'phone_number': phone_number,
        'gst_number': gst_number,
        'status': status,
        'profile_picture': profile_picture,
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

@allowed_users(allowed_roles=['SUPPLIER'])
def all_orders(request):
    orders = SupplierOrder.objects.filter(supplier=request.user)
    context = {'orders': orders}
    return render(request, 'all_orders.html', context)


# Manufacturer

@allowed_users(allowed_roles=['MANUFACTURER'])
def manufacturer_home(request):
    text_ = {'search_with_product_name_or_category':"search_with_product_name_or_category"}
    return render(request, 'manufacturer_home.html',text_)

@allowed_users(allowed_roles=['MANUFACTURER'])
def search_supplier(request):
    search_query = request.GET.get('search_box')
    supplier_products = SupplierProduct.objects.filter(Q(name__icontains=search_query) | Q(type__icontains=search_query))
    suppliers = SupplierDetails.objects.filter(user__supplierproducts__in=supplier_products)
    supplier_data = []
    suppliers_list = []
    for supplier in suppliers:
        if supplier not in suppliers_list:
            suppliers_list.append(supplier)
            supplier_products = supplier.user.supplierproducts.filter(Q(name__icontains=search_query) | Q(type__icontains=search_query))
            supplier_data.append({'supplier': supplier, 'products': supplier_products})

    context = {'supplier_data': supplier_data}  
    return render(request, 'manufacturer_home.html', context)

@allowed_users(allowed_roles=['MANUFACTURER'])
def manufacturer_profile(request):
    #To check if supplier details already exist
    user_details = 'disp_mode'
    try:
        supplier_profile = SupplierDetails.objects.get(user=request.user)
        address = supplier_profile.address
        contact_person = supplier_profile.contact_person
        phone_number = supplier_profile.phone_number
        gst_number = supplier_profile.gst_number
        status = supplier_profile.status
        print(status)
        profile_picture = supplier_profile.profile_pic.url if supplier_profile.profile_pic else None
        if request.method == 'POST':
            if 'edit' in request.POST:
                user_details = 'edit_mode'
            elif 'submit' in request.POST:
                supplier_profile.address = request.POST['address']
                supplier_profile.contact_person = request.POST['contact_person']
                supplier_profile.phone_number = request.POST['phone_number']
                supplier_profile.gst_number = request.POST['gst_number']
                supplier_profile.status = 'Pending' # give P in caps or will get error
                print(supplier_profile.status)
                # Get and validate the profile picture
                profile_picture = request.FILES.get('profile_picture')
                print(profile_picture)
                if profile_picture:
                    supplier_profile.profile_pic = profile_picture
                supplier_profile.save()
                print(supplier_profile.status)
                address = supplier_profile.address
                contact_person = supplier_profile.contact_person
                phone_number = supplier_profile.phone_number
                gst_number = supplier_profile.gst_number
                status = supplier_profile.status                
                profile_picture = supplier_profile.profile_pic.url if supplier_profile.profile_pic else None
                messages.success(request, 'Profile updated successfully!')
                user_details = 'disp_mode'
    except SupplierDetails.DoesNotExist:
        if request.method == 'POST':
            if 'submit' in request.POST:
                address = request.POST['address']
                contact_person = request.POST['contact_person']
                phone_number = request.POST['phone_number']
                gst_number = request.POST['gst_number']
                # Get and validate the profile picture
                profile_picture = request.FILES.get('profile_picture')
                supplier_profile = SupplierDetails(user=request.user,
                                                   address= address,
                                                   contact_person= contact_person,
                                                   phone_number= phone_number,
                                                   gst_number= gst_number,
                                                   status='Pending')
                if profile_picture:
                    supplier_profile.profile_pic = profile_picture
                supplier_profile.save()
                messages.success(request, 'Profile created successfully!')
                user_details = 'disp_mode'
        else:
            user_details = 'edit_mode'
            address = ''
            contact_person = ''
            phone_number = ''
            gst_number = ''
            status = 'Pending'
            profile_picture = None
    context = {
        'user_details': user_details,
        'address': address,
        'contact_person': contact_person,
        'phone_number': phone_number,
        'gst_number': gst_number,
        'status': status,
        'profile_picture': profile_picture,
    }
    return render(request, 'manufacturer_profile.html', context)

@require_POST
@allowed_users(allowed_roles=['MANUFACTURER'])
def add_to_cart(request):
    # Get the product and quantity from the POST request.
    print("add to cart")
    # print(request.POST)
    product_id = request.POST['product_id']
    quantity = int(request.POST['quantity'])
    totalAmount = float(request.POST['total_amount'])
    supplier_name = str(request.POST['supplier_name'])
    # Get the product and calculate the total amount.
    product = get_object_or_404(SupplierProduct, id=product_id)
    supplier = User.objects.get(username=supplier_name)
    total_amount = quantity * product.price
    print(totalAmount,supplier)
    # Check if there is an existing order for the product.
    try:
        order = SupplierOrder.objects.get(product=product, status=SupplierOrder.PENDING, manufacturer_or_retailers=request.user,supplier=supplier)
        # If there is an existing order, update the quantity and total amount.
        order.quantity += quantity
        order.totalamount += total_amount
        order.save()
    except SupplierOrder.DoesNotExist:
        # If there is no existing order, create a new one.
        order = SupplierOrder.objects.create(
            manufacturer_or_retailers=request.user,
            supplier=supplier,
            product=product,
            quantity=quantity,
            totalamount=total_amount
        )

    # Return a JSON response with the order details.
    return JsonResponse({
        'success': True,
        'order_id': order.id,
        'product_name': product.name,
        'quantity': order.quantity,
        'total_amount': order.totalamount,
    })

@allowed_users(allowed_roles=['MANUFACTURER'])
def order_list(request):
    orders = SupplierOrder.objects.filter(Q(manufacturer_or_retailers=request.user) & Q(order_status='in_cart'))
    context = {'orders': orders}
    return render(request, 'order_list.html', context)

def order_details(request, order_id):
    # if not request.user.is_superuser:
    #     return redirect('home')
    print("Now",order_id)
    order = get_object_or_404(SupplierOrder, id=order_id)
    print("debug")
    if request.method == 'POST':
        if 'Completed' in request.POST:
            order.status = 'Completed'
            order.save()
            # send email to supplier notifying them of approval
            return redirect('/all_orders')
        elif 'Cancelled' in request.POST:
            order.status = 'Cancelled'
            order.save()
            # send email to supplier notifying them of rejection
            return redirect('/all_orders')

    context = {
        'order': order
    }

    return render(request, 'order_details.html', context)

def remove_from_cart(request, order_id):
    # Get the order to be removed from the database
    order = get_object_or_404(SupplierOrder, id=order_id, manufacturer_or_retailers=request.user, order_status='in_cart')

    # If the request is a POST, delete the order and redirect to cart page
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order removed from cart successfully.')
    
    return redirect('/orders')
    


# Retailer

@allowed_users(allowed_roles=['RETAILER'])
def retailer_home(request):
    return render(request, 'retailer_home.html')

# Admin items



def supplier_admin(request):
    # Get all suppliers with a status of "pending"
    # if not request.user.is_superuser:
    #     return redirect('home')
    suppliers = SupplierDetails.objects.filter(user__role='SUPPLIER')
    print(suppliers)

    context = {
        'suppliers': suppliers
    }

    return render(request, 'supplier_admin.html', context)

def manufacturer_admin(request):
    # Get all suppliers with a status of "pending"
    # if not request.user.is_superuser:
    #     return redirect('home')
    suppliers = SupplierDetails.objects.filter(user__role='MANUFACTURER') 
    print(suppliers)

    context = {
        'suppliers': suppliers
    }

    return render(request, 'manufacturer_admin.html', context)

def retailer_admin(request):
    # Get all suppliers with a status of "pending"
    # if not request.user.is_superuser:
    #     return redirect('home')
    suppliers = SupplierDetails.objects.filter(user__role='RETAILER') 
    print(suppliers)

    context = {
        'suppliers': suppliers
    }

    return render(request, 'retailer_admin.html', context)

# @login_required
def supplier_details(request, supplier_id):
    # if not request.user.is_superuser:
    #     return redirect('home')
    print(supplier_id)
    supplier = get_object_or_404(SupplierDetails, id=supplier_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            supplier.status = 'Approved'
            supplier.save()
            # send email to supplier notifying them of approval
            return redirect('/supplier_admin')
        elif 'reject' in request.POST:
            supplier.status = 'Rejected'
            supplier.save()
            # send email to supplier notifying them of rejection
            return redirect('/supplier_admin')

    context = {
        'supplier': supplier
    }

    return render(request, 'supplier_details.html', context)

def manufacturer_details(request, supplier_id):
    # if not request.user.is_superuser:
    #     return redirect('home')
    print(supplier_id)
    supplier = get_object_or_404(SupplierDetails, id=supplier_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            supplier.status = 'Approved'
            supplier.save()
            # send email to supplier notifying them of approval
            return redirect('/manufacturer_admin')
        elif 'reject' in request.POST:
            supplier.status = 'Rejected'
            supplier.save()
            # send email to supplier notifying them of rejection
            return redirect('/manufacturer_admin')

    context = {
        'supplier': supplier
    }

    return render(request, 'manufacturer_details.html', context)

def retailer_details(request, supplier_id):
    # if not request.user.is_superuser:
    #     return redirect('home')
    print(supplier_id)
    supplier = get_object_or_404(SupplierDetails, id=supplier_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            supplier.status = 'Approved'
            supplier.save()
            # send email to supplier notifying them of approval
            return redirect('/retailer_admin')
        elif 'reject' in request.POST:
            supplier.status = 'Rejected'
            supplier.save()
            # send email to supplier notifying them of rejection
            return redirect('/retailer_admin')

    context = {
        'supplier': supplier
    }

    return render(request, 'retailer_details.html', context)

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