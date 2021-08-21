from django import forms
from accounts.models import *
from training.models import *
from django.conf import settings

class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = TrainingProvider
        fields = "__all__"

class NewCourseForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.SelectDateWidget)
    end_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.SelectDateWidget)
    class Meta:
        model = Course
        exclude = ["student_numbers"]

class NewStudentToCourseForm(forms.ModelForm):
    class Meta:
        model = UserCourse
        fields = "__all__"

class NewDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name"]

class EditStudentDepartmentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "family_name", "username", "department", "count_trainings"]

