from django import forms # forms enables us to create form fields and editing the field input types.
from .models import Task # Importing Task model (Task table in db)


class TaskForm(forms.ModelForm):
    """Creating a Task Model Form for Creating TAsks, Model Form creates a form depending on Task table schema"""
    class Meta:
        model = Task # indicating the model we want to create a form for.
        exclude = ["user","created_date"] # indicating which fields we don't want a user to fill
        # which are the user object, in the views.py we set it to the user object of the request (set to the user who requests to create a task)
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control", "placeholder":"Title", "aria-label":"Title"}),
            "description": forms.Textarea(attrs={"class":"form-control","placeholder:":"Leave a comment here","id":"floatingTextarea"}),
            "deadline_date": forms.DateTimeInput(attrs={"type":"datetime-local","class":"form-control"}),
        } # widgets enables us to edit the form fields as html and fields types
        # I'm using Bootstrap
