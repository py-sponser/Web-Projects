from django.urls import path
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views # import views of auth models where classes of reset password classes exist





urlpatterns = [
    path('account/register/',accounts_views.register,name="register"), # url path to registration page, name is used to be called in the template to execute the register function
    
    path('account/login/',accounts_views.user_login,name="login"), # url path to login page, name is used to be called in the template to execute the login function
    
    path('logout/',accounts_views.user_logout,name="logout"), # url path to logout, name is used to be called in the template to execute the logout function
    
    path("account/settings/",accounts_views.account_settings,name="settings"), # url to setting page, name is used to be called in the template to execute the account_settings function



    # Resetting password feature is added using the builtin django classes mentioned here
    path("reset_password/",auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="password_reset"),
    # Password Reset View is a class based view that renders a template with a form for giving email address to send email to it with a link to reset password

    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_password_sent.html"),name="password_reset_done"),
    #Password Reset Done View is a class which renders a template with a message after an email has been sent to the registered user

    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name="password_reset_confirm"),
    # Password Reset Confirm View is a class which displays a form of setting new password 
    
    path("reset_password_complete/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_complete"),
    # Password Reset Done View is a class which renders a template with a message after all process has been done 
]