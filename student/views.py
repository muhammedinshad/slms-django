from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .form import RegistrationForm, LoginForm,ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from principal.models import Department, AddOnCourse, Enrollment
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .decorators import student_required

def welcome(request):
    return render(request, "welcome.html")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['firstname'],
                last_name=form.cleaned_data['lastname'],
            )

            student = form.save(commit=False)
            student.user = user
            student.role = 'student'
            student.save()

            try:
                send_mail(
                subject="Welcome...",
                message=f"Hi {user.first_name}...👋 welcome to Student Portal",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            except Exception as e:
                print("Email error:", e)
            messages.success(request, "Registration Successful! Please login.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                student = user.student
                if student.role == "principal":
                    login(request, user)
                    return redirect("principal_dashboard")
                else:
                    if student.is_blocked:
                        messages.error(request, "Your account is blocked.")
                        return redirect("login")
                    else:
                        login(request, user)
                        messages.success(request, f"Welcome back, {user.username}!")
                        return redirect("student_dashbord")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Please fill in all fields correctly.")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@student_required
def student_dashbord(request):
    student = request.user.student
    
    enrollments = Enrollment.objects.filter(student=student)
    
    accepted_count = enrollments.filter(status='accepted').count()
    pending_count = enrollments.filter(status='pending').count()
    rejected_count = enrollments.filter(status='rejected').count()
    
    context = {
        'enrollments': enrollments,
        'accepted_count': accepted_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
    }
    
    return render(request, "student_dashbord.html", context)

@student_required
def course_list(request):
    """Display all available courses with filtering and direct enrollment"""
    student = request.user.student
    courses = AddOnCourse.objects.all().select_related('department')
    departments = Department.objects.all()
    
    department_filter = request.GET.get('department')
    if department_filter:
        courses = courses.filter(department_id=department_filter)

    search_query = request.GET.get('search')
    if search_query:
        courses = courses.filter(
            Q(course_name__icontains=search_query) | 
            Q(course_description__icontains=search_query)
        )
    
    # Get already enrolled course IDs
    enrolled_course_ids = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)
    
    # ADD PAGINATION - 10 courses per page
    paginator = Paginator(courses, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'courses': page_obj,  
        'departments': departments,
        'enrolled_course_ids': list(enrolled_course_ids),
        'page_obj': page_obj,  
    }
    
    return render(request, "purchase_course.html", context)

@student_required
def enroll_course(request, course_id):
    """Enroll student in a course - handles POST only"""
    if request.method != "POST":
        return redirect('course_list')
    
    student = request.user.student
    course = get_object_or_404(AddOnCourse, id=course_id)
    
    # Check if already enrolled
    already_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
    
    if already_enrolled:
        messages.warning(request, "You are already enrolled in this course!")
        return redirect('course_list')
    
    # Create enrollment
    Enrollment.objects.create(
        student=student,
        course=course,
        status='pending'
    )
    
    messages.success(request, f"Successfully enrolled in {course.course_name}! Your enrollment is pending approval.")
    return redirect('student_dashbord')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

@student_required
def profile(request):
    student = request.user.student
    return render(request, "profile.html", {"student": student})

@student_required
def edit_profile(request):
    student = request.user.student

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=student)

    return render(request, "edit_profile.html", {"form": form})

@student_required
def delete_enrollment(request, id):
    enrollment = get_object_or_404(
        Enrollment,
        id=id,
        student=request.user.student
    )

    if request.method == "POST":
        enrollment.delete()
    return redirect("student_dashbord")