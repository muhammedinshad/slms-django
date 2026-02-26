from django import forms
from .models import AddOnCourse, Department

class AddOnCourseForm(forms.ModelForm):
    class Meta:
        model = AddOnCourse
        fields = ['course_name', 'course_description', 'course_price','department']
        widgets = {
            'course_description': forms.Textarea(attrs={'rows': 4}),
        }
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"