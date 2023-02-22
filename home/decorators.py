from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

# its a wrapper fucntion(which takes function as parameter and do some checks before calling the actual function
def unauthenticateduser(view_func):
    def wrapper_func(request,*args,**kwargs):
        if(request.user.is_authenticated):
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
            return view_func(request, * args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]): # single page can allow mulitple types of users
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            #I we can write the logic here
            user = request.user
            group = None
            role_list = []
            if request.user.groups.exists():
                group = str(request.user.groups.all()[0])
            print("role of user accessing the page",str(group))
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("you are not allowed to access this page")
        return wrapper_func
    return decorator
