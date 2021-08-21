from django.shortcuts import redirect
from django.http import HttpResponse

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request,*args,**kwargs)
        else:
            return HttpResponse("<h3 style='text-align:center;color:darkred;'>You are not authorized to access this page.</h3>")

    return wrapper_func