from django.urls import path
from training import views

app_name = "training"

urlpatterns = [
    path("", views.home, name="home"),
    path("courses/", views.get_courses, name="get_courses"),
    path("courses/<str:course_name>/details/", views.get_course_details, name="get_course_detail"),
    path("courses/enroll/", views.create_user_course, name="create_user_course"),
    path("user/courses/registered/", views.user_registered_courses, name="user_registered_courses"),
    path("courses/<str:student_id>/<str:course_name>/quit/", views.quit_course, name="quit_course"),
    path("student/profile/", views.get_profile_info, name="get_profile_info"),
]