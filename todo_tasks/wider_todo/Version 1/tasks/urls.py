from django.urls import path
from tasks import views as task_views # importing views of task app

urlpatterns = [ 
    
    
    path('task/<pk>/update/',task_views.update_task,name="update_task"), # url path to task update page, recieving id/pk from page when calling the update task function
    
    path('create_task/',task_views.create_task,name="create_task"), # url path to create task page, name is used to be called in the template to execute the views.create_task function
    
    path("task/<pk>/delete/",task_views.delete_task,name="delete_task"), # url path to delete task, name is used to be called in the template to execute the delete_task function
    
]