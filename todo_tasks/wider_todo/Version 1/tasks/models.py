from django.db import models # importing models class that enables us to create tables, fields in the database.
from django.contrib.auth.models import User # importing the ready user model builtin of django for User Management.
from django.utils import timezone # importing timezone to use it for setting dates.


class Task(models.Model):
    """Creating a task table in the database"""
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE) # each registered user can have many tasks.
    title = models.CharField(max_length=30) # each task has a title.
    description = models.TextField(max_length=200, default=None) # each task has a description.
    created_date = models.DateTimeField(default=timezone.now) # each task has a created date.
    deadline_date = models.DateTimeField(null=True) # each task has a deadline date (for notification system).
    completed = models.BooleanField() # each task has a status whether user completed it or not.

    def __str__(self):
        """returning a string representation for each row of data in the table"""
        return f"[User ID: {self.user.id}] [Username: {self.user.username}] [Title: {self.title}]"
