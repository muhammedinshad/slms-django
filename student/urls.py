from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    
    path('student_dashbord/', views.student_dashbord, name='student_dashbord'),  
    
    path('profile/', views.profile, name='profile'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # Course Purchase URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('delete-enrollment/<int:id>/', views.delete_enrollment, name='delete_enrollment'),  
]