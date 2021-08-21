from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def restrict_after_authenticate(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("training:home")
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func



