from django.http import HttpResponse
from django.shortcuts import redirect

# its a wrapper fucntion(which takes function as parameter and do some checks before calling the actual function
def unauthenticateduser(view_func):
    def wrapper_func(request,*args,**kwargs):
        if(request.user.is_authenticated):
            return redirect('admin_home')
        else:
            return view_func(request, * args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]): # single page can allow mulitple types of users
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            #I we can write the logic here
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                # print("the group of user who is logged in is",group)
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("you are not allowed to access this page")
        return wrapper_func
    return decorator
