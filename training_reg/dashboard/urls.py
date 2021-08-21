from django.urls import path
from dashboard import views


app_name = "dashboard"

urlpatterns = [
    # Queries Links
    path("dashboard/", views.dashboard_lists, name="dashboard_lists"),
    path("dashboard/<str:company_name>/courses/", views.get_company_courses, name="company_courses"),
    path("dashboard/course/<str:course_name>/", views.get_course_details, name="course_detail"),
    path("dashboard/<str:course_name>/registered_students/", views.get_course_registered_students, name="get_course_registered_students"),
    path("dashboard/training/get_student_training_pass_status/", views.get_student_training_pass_status, name="get_student_training_pass_status"),
    path("dashboard/<str:department_name>/companies/", views.get_department_companies, name="get_department_companies"),
    path("dashboard/<str:department_name>/students/", views.get_department_students, name="get_department_students"),



    # Forms
    path("dashboard/add_company/", views.add_company, name="add_company"),
    path("dashboard/add_course/", views.add_course, name="add_course"),
    path("dashboard/add_new_department/", views.add_new_department, name="add_new_department"),
    path("dashboard/add_student_to_course/", views.add_student_to_course, name="add_student_to_course"),


    # Editing and Deletion

    # Deletion
    path("dashboard/company/<str:company_name>/delete/", views.delete_company, name="delete_company"),
    path("dashboard/course/<str:course_name>/delete/", views.delete_course, name="delete_course"),
    path("dashboard/department/<str:department_name>/delete/", views.delete_department, name="delete_department"),
    path("dashboard/student_course/<int:student_id>/<str:course_name>/delete/", views.delete_student_from_course, name="delete_student_from_course"),

    # Editing
    path("dashboard/course/<str:course_name>/edit/", views.edit_course, name="edit_course"),
    path("dashboard/department/<str:department_name>/edit/", views.edit_department, name="edit_department"),
    path("dashboard/student_course/<int:student_id>/<str:course_name>/edit/", views.edit_student_course, name="edit_student_course"),
    path("dashboard/department/student/<int:student_id>/edit/", views.edit_student_department, name="edit_student_department"),


]