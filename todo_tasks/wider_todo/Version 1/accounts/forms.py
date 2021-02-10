from django import forms # forms enables us to create form fields and editing the field input types.
from django.contrib.auth.models import User # importing the User model that enables us to create/fetch users (built in user table)


class UserForm(forms.ModelForm):
    """Creating a User Model Form for registration, Model Form creates a form depending on Task table schema"""
    class Meta:
        model = User # indicating the model we want to create a form for.
        fields = ("first_name","last_name","username","email") # specifying the fields we want a user to fill in the form
        widgets = {
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.TextInput(attrs={"class":"form-control"}),
        } # widgets enables us to edit the form fields as html and fields types
        # I'm using Bootstrap
