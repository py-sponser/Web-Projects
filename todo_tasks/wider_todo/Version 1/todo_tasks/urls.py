"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # importing admin to register the admin url for admin page
from django.urls import path, include # import path function to set url paths and what functions to be executed when http recievign requests
from tasks.views import index

urlpatterns = [
    path('admin/', admin.site.urls), # url path to admin page executing admin.site.urls function
    path("",index,name="index"), # url path to home page, name is used to be called in the template to execute views.index function
    path("",include("accounts.urls")),
    path("",include("tasks.urls")),
]
