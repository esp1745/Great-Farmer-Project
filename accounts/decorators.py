from django.shortcuts import redirect
from django.http import HttpResponse




def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwarges):
        if request.user.is_authenticated:
            return redirect('home')
        else:
           return view_func(request, *args, **kwarges)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwarges):
            
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args, **kwarges)
           
            else:
               return HttpResponse('you are not authorized to view this page!!!')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwarges):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'Farmer':
            return redirect('home')
        if group == 'Customer':
            return view_func(request, *args, **kwarges)
    return wrapper_function
        