from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.

@api_view(["GET"])
def tasklist(request):
    """Returns Tasks (in json format) only if request is GET"""
    tasks = models.Task.objects.all().order_by("-id")
    serializer = TaskSerielizer(tasks, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def taskDetail(request,pk):
    """Returns info of 1 task (in json format) only if request is GET """
    task = models.Task.objects.get(id=pk)
    serializer = TaskSerielizer(task,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def taskCreate(request):
    """Returns the new task info (in json format) after creating it, request method sent from frontend must be POST"""
    serializer = TaskSerielizer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(["POST"])
def taskUpdate(request,pk):
    """Returns the new task info updated (in json format) after updating it, request method sent from frontend must be POST"""
    task = models.Task.objects.get(id=pk)
    serializer = TaskSerielizer(instance=task,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(["DELETE"])
def taskDelete(request,pk):
    """Returns a message after deleting a task, request method sent from frontend must be DELETE"""
    task = models.Task.objects.get(id=pk)
    task.delete()
    
    return Response("Item deleted successfully.")