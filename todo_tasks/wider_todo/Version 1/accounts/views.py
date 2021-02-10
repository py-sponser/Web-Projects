from django.shortcuts import render, redirect
# Importing render to render requests, templates, and data fetched from the database (sending them as context dictionary to the page.)
# Importing redirect which enables us to redirect a current page to other page we specify.

from .forms import UserForm

from django.contrib.auth.models import User
# importing the user model to fetch/create users from/to the db"""

from django.contrib.auth.decorators import login_required
# Importing login_required to limit user navigation in the page, cannot see contents until he signs in

from django.contrib import messages
# messages are to display messages in the page to the user if any error occurs.

from django.contrib.auth import login, logout, authenticate
# Importing login, logout, and authenticate functions that are responsible of logging in, logging out, and authentication.
from django.http import HttpResponseRedirect
from django.urls import reverse
# HttpResponseRedirect is similar to redirect and often used with reverse (not to hardcode the path of url, just using name of path in urls.py directly)
# reverse is used to indicate the url to be redirected to with args and kwargs.

from accounts.decorators import authenticated
# authenticated: invented decorator to indicated whether the user is authenticated or not to limit unlogical navigations in the page.
from django.contrib.auth.forms import PasswordChangeForm
# Password Change Form: builtin django class used to display a form for changing password of user.
from django.contrib.auth.views import update_session_auth_hash
# update_session_auth_hash: is used to update the session of the user after changing password not to be logged out.

# Create your views here.
def account_settings(request):
    """Enables the user to change profile info and change password"""
    user_info_form = UserForm(instance=request.user) # display a form of user info with displaying last saved info (instance of saved info in db))
    change_password_form = PasswordChangeForm(request.user) # display a form of changing password that belongs to the user loggedin (which exists in the request)
    if request.method == "POST": # if incoming request method is POST (which is sent by html form)
        if "old_password" not in request.POST: # this check prevents clearing the profile info when password change form is submitted.
            # if we don't make this check, the profile form would send empty values for profile data (except username). 
            user_info_form = UserForm(request.POST, instance=request.user) # pass the request POST data to the django form to be handled with instance of data that hasn't got changed
            if user_info_form.is_valid(): # validating the form, if true:
                user_info_form.save(commit=True) # the django form save function saves the content to the database
                messages.success(request, "[+] Your profile got successfully updated") # creating a success message to be displayed for the user in the page.
                return redirect("settings") # redirecting to the same page of settings (the purpose is refreshing).

        change_password_form = PasswordChangeForm(request.user, request.POST) # pass the request POST data to the django from to be handled with data of the user (request.user)
        if change_password_form.is_valid(): # validating the form, if true:
            user = change_password_form.save() # saving new password to the db, making object of django form and its save function to have the object responsible of making operations like save function later on.
            update_session_auth_hash(request, user) # updating the user session after saving the new password not to be logged out (passing the request and the user object (contain info about the user and the request))
            user.save() # saving all changes (new session and new password completely.)
            messages.success(request, "[+] Your password was successfully changed!") # creating a success message to be displayed for the user in the page.
            return redirect("settings") # redirecting to the same page of settings (the purpose is refreshing).
        else: # if change password form is not validated
            messages.info(request, '[-] Data is not valid.') # creating an info message to be displayed for the user in the page.
            return redirect("settings") # redirecting to the same page of settings (the purpose is refreshing).

            
    context = {"user_form": user_info_form, "password_form": change_password_form} 
    return render(request, "accounts/account_settings.html",context) # returning rendering the request, the template (page content), and the forms as context dictionary.

@login_required(login_url="login") # a user can only loggout when he's loggedin!
def user_logout(request):
    """Logging user out """
    logout(request) # it sets the user model of the request to None and removes the session info.
    return redirect("index") # redirect to home page


@authenticated # if a user is loggedin, he cannot make requests to register or login page
def user_login(request):
    """Login the user in"""
    if request.method == "POST": # if request method is POST: (which is sent by html form)
        # I don't use django form, I made and html form, recieving and validating data from here.
        username = request.POST.get("username") # getting username from the request.
        password_login = request.POST.get("password") # getting password from the request
        if User.objects.filter(username=username): # checking if the user is registered in the system or not by searching for its username in the db.
            user = authenticate(username=username, password=password_login) # authenticate the user, check for the credentials
            if user: # if credentials are true
                if user.is_active: # if user account is active (activated)
                    login(request, user) # log the user in, set the user object the user who logs in and create session for him.
                    return HttpResponseRedirect(reverse('index')) # redirect to home page
                else: # if user is not active
                    messages.info(request, "Account hasn't been activated yet.") # create a message for the user.
                    return redirect("login") # redirect to the login page
            else: # if credentials is wrong
                messages.info(request, "Username or Password is incorrect.") # create a message for the user
                return redirect("login") # redirect to login page
        else: # if username is not found in db
            messages.info(request, "Account is not exist.") # create a message for the user
            return redirect("login") # redirect to login page
    else: # if request is not POST:
        return render(request, "accounts/login.html") # return rendering the request and the template.


def password_validation(password):
    """Checking password requirements for validation when registering account"""
    special_symbols = ["!", '$', '@', '#', '%', "^", "&", "*", "(", ")", "-", "=", "+", "_", "/", "<", ">", ":", ","]
    # symbols to use for checking whether a password contain symbols or not.
    status = True # boolean variable used for checking

    if len(password) < 7: # password length should be greater than 7
        status = False

    if len(password) > 15: # password length should be lower than 15
        status = False

    if not any(char.isdigit() for char in password): # checking each char in the password if there's a number or not
        status = False

    if not any(char.isupper() for char in password): # checking each char in the password if there's an uppercase letter or not
        status = False

    if not any(char.islower() for char in password): # checking each char in the password if there's an lowercase letter or not
        status = False

    if not any(char in special_symbols for char in password): # checking each char in the password if there's a symbol or not
        status = False
    if status: # if all requirements exist:
        return status # returning True


@authenticated # if a user is loggedin, he cannot make requests to register or login page
def register(request):
    """Handling registration accounts"""
    if request.method == "POST":  # if request method is POST: (which is sent by html form)
        firstname = request.POST.get("firstname") # getting first name form request
        lastname = request.POST.get("lastname") # getting last name form request
        user_name = request.POST.get("username") # getting username form request
        password_1 = request.POST.get("password1") # getting password1 form request
        password_2 = request.POST.get("password2") # getting password2 form request
        e_mail = request.POST.get("email") # getting email from the request
        if firstname and lastname and user_name and password_1 and password_2 and e_mail:
            # if fields we try to get are fetched:
            if password_1 == password_2: # verifying password
                check = password_validation(password_1) # validating password by calling that written password_validation function.
                if check: # if check = status   = True
                    if User.objects.filter(username=user_name).exists(): # if username is already exist
                        messages.info(request, "[-] Username is already taken") # creating a message for the user
                        return redirect("register") # redirect to the same page (refreshing)
                    if User.objects.filter(email=e_mail).exists(): # if email is already exist
                        messages.info(request, "[-] Email is already taken.") # creating a message for the user
                        return redirect("register") # redirect to the same page (refreshing)
                    else: # if it's a completely new user
                        user = User.objects.create_user(username=user_name, password=password_1, email=e_mail,
                                                        first_name=firstname, last_name=lastname) # creating new user with given data.
                        
                        user.save() # saving user and its data to the db.

                        messages.success(request, "[+] Account has been registered successfully.") #  creating success message for the user

                        return redirect("register") # refreshing the page
                else: # if data requirements are not valid.
                    messages.info(request, "[-] Invalid Data Requirements.") # creating a message for the user
                    return redirect("register") # refreshing the page
            else: # if 2 passwords are not equal 
                messages.info(request, "[-] Password is not match.") # creating a message for the user
                return redirect("register") # refreshing the page
        else: # if any field of the fields is empty (giving no data)
            messages.info(request, "[-] Please, Fill empty fields") # creating a message for the user
            return redirect("register") # refreshing the page
    else: # if request is not POST
        # displaying data requirements for the user when filling the registration form!
        requirements = """
                                    [-] Password length shouldn't be fewer than 9.
                                    [-] Password length shouldn't be greater than 15.
                                    [-] Password should contain numbers.
                                    [-] Password should have contain capitalized letters.
                                    [-] Password should have lowercase letters.
                                    [-] Password should contain special characters, as !@#$%.. .
                                    """
        return render(request, "accounts/registeration.html", {"requirements": requirements}) # return rendering the request, template and requiremnts to the page.
