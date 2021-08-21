from django.shortcuts import render, redirect
from training.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import restrict_after_authenticate
# Create your views here.
from accounts.utils import password_validation
import random


@restrict_after_authenticate
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("login")
        password = request.POST.get("password")
        if username and password:
            try:
                if User.objects.filter(username__iexact=username) or User.objects.filter(email__iexact=username) \
                        or User.objects.filter(id=int(username)):
                    if username.isdigit():
                        username = int(username)
                        username = User.objects.get(id=username).username
                    elif "@" in username:
                        username = User.objects.get(email=username).username
                    else:
                        username = request.POST.get("login")
                    user = authenticate(username=username, password=password)
                    if user:
                        if user.is_active:
                            login(request, user)
                            return redirect("training:home")

                        else:
                            messages.error(request, "Account hasn't been activated yet.")
                            return redirect("accounts:login")
                    else:
                        messages.error(request, "Username or Password is incorrect.")
                        return redirect("accounts:login")
                else:
                    messages.error(request, "Account is not exist.")
                    return redirect("accounts:login")
            except:
                messages.error(request, "Account is not exist.")
                return redirect("accounts:login")
        else:
            messages.error(request, "Fields are not filled.")
            return redirect("accounts:login")
    else:
        return render(request, "accounts/login.html")

@login_required(login_url="accounts:login")
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("training:home")
    else:
        return redirect("training:home")


@restrict_after_authenticate
def register(request):
    departments = Department.objects.all()
    if request.method == "POST":
        id = random.randint(100,20000)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        family_name = request.POST.get("family_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        department = request.POST.get("department")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if first_name and last_name and username and email and password1 and password2 and department != "Select Department":
            if password1 == password2:
                check = password_validation(password1)
                if check:
                    if not Department.objects.filter(name=department).exists():
                        messages.error(request, f"No Department called {department}")
                        return redirect("accounts:register")

                    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or User.objects.filter(id=id).exists():
                        messages.error(request, f"This email is already used with an account.")
                        return redirect("accounts:register")



                    else:
                        user = User.objects.create_user(id=id, username=username, first_name=first_name, last_name=last_name,
                                                        family_name=family_name, email=email, password=password1,
                                                        is_active=True)

                        user.set_password(password1)
                        department = Department.objects.get(name=department)
                        user.department = department
                        user.save()

                        new_user = authenticate(username=username, password=password1)
                        login(request,new_user)
                        return redirect("training:home")

                else:
                    messages.error(request,"[-] Password requirements are not applied.")  # creating a message for the user
                    return redirect("accounts:register")  # refreshing the page
            else:
                messages.error(request, "[-] Password is not match.")  # creating a message for the user
                return redirect("accounts:register")  # refreshing the page
        else:
            messages.error(request, "[-] Please, Fill empty fields")  # creating a message for the user
            return redirect("accounts:register")  # refreshing the page
    else:
        requirements = """
[-] Password length shouldn't be fewer than 9.
[-] Password length shouldn't be greater than 15.
[-] Password should contain numbers.
[-] Password should have contain capitalized letters.
[-] Password should have lowercase letters.
[-] Password should contain special characters, as !@#$%.. .
                                            """
        context = {"requirements": requirements, "departments":departments}
        return render(request, "accounts/register.html", context)  # return rendering the request, template and requiremnts to the page.
