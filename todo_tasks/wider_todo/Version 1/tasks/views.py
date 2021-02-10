from django.shortcuts import render, redirect
# Importing render to render requests, templates, and data fetched from the database (sending them as context dictionary to the page.)
# sImporting redirect which enables us to redirect a current page to other page we specify.

from tasks.forms import TaskForm
# Importing forms we created for registerations and creating tasks.
from tasks.models import Task
# Importing the Task mode (Table in db) to fetch/create tasks from/to the db"""
from django.contrib.auth.decorators import login_required
# Importing login_required to limit user navigation in the page, cannot see contents until he signs in


from django.contrib import messages
# messages are to display messages in the page to the user if any error occurs.

from django.contrib.auth.models import User
# importing the user model to fetch/create users from/to the db"""


def index(request):
    """Returns a list of all tasks of the logged in user only to home page."""
    user_tasks = Task.objects.all().filter(user=request.user.id).order_by("-created_date") # listing all tasks that belongs to the logged in user ordered by the newest tasks.
    return render(request, "index.html", {"tasks": user_tasks}) # returning rendering the request, the template (page content) and the list of tasks as context dictionary.


@login_required(login_url="login") # whenever a user enters a page that requires to be loggedin, he gets redirected to login page.
def update_task(request, pk):
    """Updates specific task requested to be updated (recieving pk/id of the task) that belongs to the loggedin user by the loggedin user"""
    task = Task.objects.get(id=pk) # getting the requested task as object by id from db.
    task_update_form = TaskForm(instance=task) # displaying a form for updating with displaying an instance of the last saved date of the task.
    if request.method == "POST": # if request method is POST (which is sent by html form):
        task_update_form = TaskForm(request.POST, instance=task) # pass the request POST data to the form and any instance of task data that hasn't got changed
        if task_update_form.is_valid(): # if form is valid:
            task_update_form.save(commit=True) # save changes recieved from the form to the database.
            return redirect("index") # redirect to home page
        else: # if form is not valid
            messages.info(request, "Invalid data requirements") # create a message to display to the user
            return redirect("update_task", pk=pk) # refresh the page of task update of its specific id/pk.
    return render(request, "tasks/task_update.html", {"form": task_update_form}) # return rendering the request, the template, and the form as context dictionary.


@login_required(login_url="login") # explained
def delete_task(request, pk):
    """Deletes specific task requested to be deleted (recieved pk/id of the task) that belongs to the loggedin user by the loggedin user"""
    task = Task.objects.get(id=pk) # getting the requested task as object by id/pk from db.
    if request.method == "POST": # if user requested an http POST request (which is sent by html form)
        task.delete() # delete the task
        return redirect("index") # redirect to the home page
    else: # if request is not POST
        return render(request, "tasks/task_delete.html", {"title": task.title}) # return rendering the request, template, and task title to inform the user which task he wants to delete, to the user browser.



@login_required(login_url="login") # explained
def create_task(request):
    """Allowing user to create new task."""
    task_create_form = TaskForm() # displaying task creation form for the user and taking it to a handler.
    if request.method == "POST":
        task_create_form = TaskForm(request.POST) # pass the request POST data to the django form.
        if task_create_form.is_valid(): # if form is valid:
            new_task = task_create_form.save(commit=False) # giving new_task handler the responsibility of what to do after validation, without commiting data the user entered to the db.
            new_task.user = request.user # setting the user of task to the loggedin user who sent the request.
            new_task.save() # commiting and saving the task to the db.
            return redirect("index") # redirect to the home page.
        else: # if form is not valid:
            messages.info(request, "Invalid data requirements.") # create a message for the user that displays after refreshing the page.
            return redirect("create_task") # redirecting the page to itself (refreshing)
    else: # if request is not POST
        return render(request, "tasks/task_create.html", {"form": task_create_form})
        # render the request, the template, and the task creation form as context dictionary to the user browser.



