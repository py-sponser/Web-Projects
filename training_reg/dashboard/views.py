from django.shortcuts import render, redirect
from training.models import *
from accounts.models import *
import json
from django.http import JsonResponse
from dashboard.forms import *
from django.contrib import messages
from dashboard.decorators import admin_only


# Create your views here.


################################################################################
# Data Editing and Deletion
############################

# Deletion
@admin_only
def delete_company(request, company_name):
    if request.method == "POST":
        company = TrainingProvider.objects.get(name__icontains=company_name)
        company.delete()
        return redirect("dashboard:dashboard_lists")
    else:
        context = {"company_name": company_name}
        return render(request, "dashboard/Data_Edit_Deletion/delete_company.html", context)


@admin_only
def delete_course(request, course_name):
    if request.method == "POST":
        course = Course.objects.get(name__icontains=course_name)
        course.delete()
        return redirect("dashboard:dashboard_lists")
    else:
        context = {"course_name": course_name}
        return render(request, "dashboard/Data_Edit_Deletion/delete_course.html", context)


@admin_only
def delete_department(request, department_name):
    if request.method == "POST":
        department = Department.objects.get(name__icontains=department_name)
        department.delete()
        return redirect("dashboard:dashboard_lists")
    else:
        context = {"department_name": department_name}
        return render(request, "dashboard/Data_Edit_Deletion/delete_department.html", context)


@admin_only
def delete_student_from_course(request, student_id, course_name):
    student = User.objects.get(id=student_id)
    if request.method == "POST":
        the_course = Course.objects.get(name__icontains=course_name)
        student_in_this_course = UserCourse.objects.get(user=student, course=the_course)
        student_in_this_course.delete()
        return redirect("dashboard:dashboard_lists")
    else:
        context = {"student_name": student.first_name + " " + student.last_name + " " + student.family_name,
                   "course_name": course_name}
        return render(request, "dashboard/Data_Edit_Deletion/delete_student_from_course.html", context)


# Edition
@admin_only
def edit_course(request, course_name):
    course = Course.objects.get(name__icontains=course_name)
    edit_course_form = NewCourseForm(instance=course)
    if request.method == "POST":
        edit_course_form = NewCourseForm(request.POST, instance=course)
        if edit_course_form.is_valid():
            edit_course_form.save()
            messages.success(request, "Course details have been successfully updated.")
            return redirect("dashboard:course_detail", course_name=course_name)
        else:
            messages.error(request, "Error Occurred, Make sure you filled all fields.")
            return redirect("dashboard:add_company")
    else:
        context = {"edit_course_form": edit_course_form, "course_name": course_name}
        return render(request, "dashboard/Data_Edit_Deletion/edit_course.html", context)


@admin_only
def edit_department(request, department_name):
    department = Department.objects.get(name__icontains=department_name)
    edit_department_form = NewDepartmentForm(instance=department)
    if request.method == "POST":
        edit_department_form = NewDepartmentForm(request.POST, instance=department)
        if edit_department_form.is_valid():
            edit_department_form.save()
            messages.success(request, "Course details have been successfully updated.")
            return redirect("dashboard:edit_department", department_name=department_name)
        else:
            messages.error(request, "Error Occurred, Make sure you filled all fields.")
            return redirect("/")
    else:
        context = {"edit_department_form": edit_department_form, "department_name": department_name}
        return render(request, "dashboard/Data_Edit_Deletion/edit_department.html", context)


@admin_only
def edit_student_course(request, student_id, course_name):
    student = User.objects.get(id=student_id)
    course = Course.objects.get(name__icontains=course_name)
    student_course = UserCourse.objects.get(user=student, course=course)
    student_course_form = NewStudentToCourseForm(instance=student_course)
    if request.method == "POST":
        student_course_form = NewStudentToCourseForm(request.POST, instance=student_course)
        if student_course_form.is_valid():
            student_course_form.save()
            messages.success(request, "Course details have been successfully updated.")
            return redirect("dashboard:get_course_registered_students", course_name=course_name)
        else:
            messages.error(request, "Error Occurred, Make sure you filled all fields.")
            return redirect("dashboard:get_course_registered_students", course_name=course_name)
    else:
        context = {"student_course_form": student_course_form,
                   "student_name": student.first_name + " " + student.last_name + " " + student.family_name,
                   "course_name": course_name}
        return render(request, "dashboard/Data_Edit_Deletion/edit_student_course.html", context)


@admin_only
def edit_student_department(request, student_id):
    student = User.objects.get(id=student_id)
    user_department_form = EditStudentDepartmentForm(instance=student)
    if request.method == "POST":
        user_department_form = EditStudentDepartmentForm(request.POST, instance=student)
        if user_department_form.is_valid():
            user_department_form.save()
            messages.success(request, "Student data have been successfully updated.")
            return redirect("dashboard:dashboard_lists")
        else:
            messages.error(request, "Error Occurred, Make sure you filled all fields.")
            return redirect("dashboard:dashboard_lists")

    else:
        context = {"user_department_form": user_department_form,
                   "student_name": student.first_name + " " + student.last_name + " " + student.family_name}
        return render(request, "dashboard/Data_Edit_Deletion/edit_user_department.html", context)


##################################################################################
# Creation Forms:
#################
@admin_only
def add_company(request):
    company_add_form = NewCompanyForm()
    if request.method == "POST":
        company_add_form = NewCompanyForm(request.POST)
        if company_add_form.is_valid():
            company_add_form.save()
            messages.success(request, "Company has been successfully added.")
            return redirect("dashboard:add_company")
        else:
            messages.error(request, "Error Occurred, Make sure you filled all fields.")
            return redirect("dashboard:add_company")
    else:
        context = {"company_add_form": company_add_form}
        return render(request, "dashboard/forms/add_company.html", context)


@admin_only
def add_course(request):
    course_add_form = NewCourseForm()
    if request.method == "POST":
        course_add_form = NewCourseForm(request.POST)
        if course_add_form.is_valid():
            course_add_form.save()
            messages.success(request, "Company has been successfully added.")
            return redirect("dashboard:add_course")
        else:
            messages.error(request, "Error Occurred, Make sure you filled all fields.")
            return redirect("dashboard:add_course")
    else:
        context = {"course_add_form": course_add_form}
        return render(request, "dashboard/forms/add_course.html", context)


@admin_only
def add_new_department(request):
    department_add_form = NewDepartmentForm()
    if request.method == "POST":
        department_add_form = NewDepartmentForm(request.POST)
        if department_add_form.is_valid():
            department_add_form.save()
            messages.success(request, "Department has been successfully added.")
            return redirect("dashboard:add_new_department")
        else:
            messages.error(request, "Error Occurred, Make sure you filled all fields.")
            return redirect("dashboard:add_new_department")
    else:
        context = {"department_add_form": department_add_form}
        return render(request, "dashboard/forms/add_new_department.html", context)


@admin_only
def add_student_to_course(request):
    add_course_student = NewStudentToCourseForm()
    if request.method == "POST":
        add_course_student = NewStudentToCourseForm(request.POST)
        if add_course_student.is_valid():
            add_course_student.save()
            messages.success(request, "Student has been successfully added to the course.")
            return redirect("dashboard:add_student_to_course")
        else:
            messages.error(request, "Error Occurred, Make sure you filled all fields.")
            return redirect("dashboard:add_student_to_course")
    else:
        context = {"add_course_student": add_course_student}
        return render(request, "dashboard/forms/add_student_to_course.html", context)


#####################################################################################
# Queries:
##########

@admin_only
def dashboard_lists(request):
    users = User.objects.all()
    providers = TrainingProvider.objects.all()  # show companies
    courses = Course.objects.all()  # show existing courses
    user_courses = UserCourse.objects.all()  # show registered courses
    departments = Department.objects.all()  # show departments and its students
    context = {"providers": providers, "courses": courses, "user_courses": user_courses, "departments": departments, "users":users}
    return render(request, "dashboard/dash_base.html", context)


@admin_only
def get_company_courses(request, company_name):
    company_courses = Course.objects.filter(provider__name__icontains=company_name)
    context = {"company_courses": company_courses}
    return render(request, "dashboard/selections/company_courses.html", context)


@admin_only
def get_course_details(request, course_name):
    course = Course.objects.get(name__icontains=course_name)
    context = {"course": course}
    return render(request, "dashboard/selections/course_detail.html", context)


@admin_only
def get_course_registered_students(request, course_name):
    user_courses = UserCourse.objects.filter(course__name__icontains=course_name)

    context = {"user_courses": user_courses, "course_name": course_name}
    return render(request, "dashboard/selections/course_registered_students.html", context)


@admin_only
def get_student_training_pass_status(request):
    data = json.loads(request.body)
    course_name = data["course_name"]
    user_id = data["user_id"]
    print(course_name, user_id)
    user_training_status = UserCourse.objects.get(course__name__icontains=course_name, user__id=user_id).course_pass
    if user_training_status or not user_training_status:
        return JsonResponse(user_training_status, safe=False)
    else:
        return JsonResponse("No Status Found.", safe=False)


@admin_only
def get_department_companies(request, department_name):
    companies = TrainingProvider.objects.filter(department__name__icontains=department_name)
    context = {"companies": companies, "department_name": department_name}
    return render(request, "dashboard/selections/department_companies.html", context)


@admin_only
def get_department_students(request, department_name):
    students = User.objects.filter(department__name__icontains=department_name)
    context = {"students": students}
    return render(request, "dashboard/selections/department_students.html", context)


