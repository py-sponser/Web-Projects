from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from training.models import *
import json
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, "training/home.html")


def get_courses(request):
    courses = Course.objects.filter(provider__department=request.user.department)
    context = {"courses":courses}
    return render(request, "training/courses_list.html", context)



def get_course_details(request, course_name):
    course = Course.objects.get(name__icontains=course_name)
    context = {"course": course}
    return render(request, "training/course_detail.html", context)


@login_required(login_url="accounts:login")
def create_user_course(request):
    data = json.loads(request.body)
    student_id = data["user_id"]
    course_name = data["course_name"]
    student = User.objects.get(id=student_id)
    course = Course.objects.get(name__icontains=course_name)
    if student.count_trainings != 2:
        if not UserCourse.objects.filter(user=student, course=course).exists():
            student_course = UserCourse.objects.create(user=student, course=course)
            student.count_trainings += 1
            student.save()
            student_course.save()
            return JsonResponse(student.count_trainings, safe=False)
        else:
            response = None
            return JsonResponse(response, safe=False)
    else:
        response = False
        return JsonResponse(response, safe=False)


@login_required(login_url="accounts:login")
def user_registered_courses(request):
    user_courses = UserCourse.objects.filter(user=request.user)
    context = {"user_courses":user_courses}
    return render(request, "training/user_registered_courses.html", context)


@login_required(login_url="accounts:login")
def quit_course(request, student_id, course_name):
    if request.method == "POST":
        student = User.objects.get(id=student_id)
        course = Course.objects.get(name__icontains=course_name)
        user_course = UserCourse.objects.get(user=student, course=course)
        if user_course.course_pass == None:
            user_course.delete()
            student.count_trainings -= 1
            student.save()
            return redirect("training:user_registered_courses")
        else:
            messages.error(request, "You cannot quit a course that you had already finished!")
            return redirect("training:user_registered_courses")
    else:
        context = {"course_name":course_name}
        return render(request, "training/quit_course.html", context)


@login_required(login_url="accounts:login")
def get_profile_info(request):
    return render(request, "training/profile.html")
