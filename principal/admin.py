from django.contrib import admin
from .models import Department, AddOnCourse, Enrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dept_name', 'dept_description']
    list_per_page = 20

@admin.register(AddOnCourse)
class AddOnCourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'department', 'course_price']
    list_filter = ['department']
    search_fields = ['course_name', 'course_description']
    list_per_page = 20
    
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'status', 'get_course_price']
    list_filter = ['status', 'enrollment_date', 'course__department']
    search_fields = ['student__user__username', 'student__firstname', 'student__lastname', 
                     'student__reg_number', 'course__course_name']
    list_editable = ['status']
    list_per_page = 20
    
    def get_course_price(self, obj):
        return f"₹{obj.course.course_price}"

    
