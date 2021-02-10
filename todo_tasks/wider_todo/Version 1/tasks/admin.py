from django.contrib import admin

# Register your models here.
from .models import Task # importing Task model (table in db)
admin.site.register(Task) # registering the task table to the admin site to be able to manage the tasks of the users.