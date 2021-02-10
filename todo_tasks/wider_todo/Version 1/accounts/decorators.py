from django.shortcuts import redirect
from django.http import HttpResponse

def authenticated(view_func): # view_func, the function after the decorator for which the decorator is called.
    """Preventing Logged in users from entering the login and register page"""
    def wrapper_func(request,*args,**kwargs):
        """Implementing what has been explained"""
        if request.user.is_authenticated: # if user is authenticated
            return redirect("index") # return to home page
        else: # if not authenticated
            return view_func(request,*args,**kwargs) # return to whatever the users requests (login or register page)
    return wrapper_func # return execution of wrapper_func


