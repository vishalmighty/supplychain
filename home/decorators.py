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
