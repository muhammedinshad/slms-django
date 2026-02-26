from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.princyDashbord, name='principal_dashboard'),  
    # Student Management
    path('student_manage/', views.student_manage, name="student_manage"),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('block-student/<int:id>/', views.toggle_block_student, name='block_student'),
    path('student/view/<int:id>/', views.student_detail, name="student_detail"),

    # Course Management
    path('add-addon-course/', views.add_addon_course, name='add_addon_course'),
    path('addon-course-list/', views.addon_course_list, name='addon_course_list'),
    path('delete-course/<int:id>/', views.delete_course, name='delete_course'),

    # Department Management
    path('add-department/', views.add_department, name="add_department"),
    
    # Enrollment Management (Accept/Reject only)
    path('enrollment/approve/<int:enrollment_id>/', views.approve_enrollment, name='approve_enrollment'),
    path('enrollment/reject/<int:enrollment_id>/', views.reject_enrollment, name='reject_enrollment'),
]