from django.urls import path
from . import views
urlpatterns = [
    path("task_list/",views.tasklist,name="task_list"),
    path("task_create/",views.taskCreate,name="task_create"),
    path("task_detail/<pk>/",views.taskDetail,name="task_detail"),
    path("task_update/<pk>/",views.taskUpdate,name="task_update"),
    path("task_delete/<pk>/",views.taskDelete,name="task_delete"),
]