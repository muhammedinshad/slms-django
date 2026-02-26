from django.shortcuts import render, redirect, get_object_or_404
from student.models import Student
from .models import AddOnCourse, Department, Enrollment
from .form import AddOnCourseForm, DepartmentForm
from django.contrib import messages
from django.db.models import Sum, Count
from student.decorators import principal_required
 
@principal_required 
def princyDashbord(request):
    std_count = Student.objects.filter(role="student").count()
    dep_count = Department.objects.all().count()
    total_courses = AddOnCourse.objects.all().count()

    departments = Department.objects.annotate(
        course_count=Count('addoncourse'),
        total_revenue=Sum('addoncourse__course_price')
    ).order_by('-course_count')
    
    all_enrollments = Enrollment.objects.all().select_related(
        'student', 'course', 'course__department'
    ).order_by('-enrollment_date')
    
    pending_count = Enrollment.objects.filter(status='pending').count()
    accepted_count = Enrollment.objects.filter(status='accepted').count()
    rejected_count = Enrollment.objects.filter(status='rejected').count()
    
    return render(request, "principal_dashbord.html", {
        "std_count": std_count,
        "dep_count": dep_count,
        "total_courses": total_courses,
        "departments": departments,
        "all_enrollments": all_enrollments,        
        "pending_count": pending_count,            
        "accepted_count": accepted_count,          
        "rejected_count": rejected_count,          
    })
 
@principal_required 
def student_manage(request):
    std = Student.objects.filter(role="student")
    return render(request, 'students_manage.html', {"std": std})

@principal_required 
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.user.delete() 
    messages.success(request, "Student deleted successfully.")
    return redirect("student_manage")

@principal_required 
def toggle_block_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.is_blocked = not student.is_blocked
    student.save()
    
    status = "blocked" if student.is_blocked else "unblocked"
    messages.success(request, f"Student {status} successfully.")
    return redirect("student_manage")

@principal_required 
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    enrollments = student.enrollments.select_related('course', 'course__department')
    accepted = enrollments.filter(  status = 'accepted')
    pending = enrollments.filter(  status = 'pending')
    rejected = enrollments.filter(  status = 'rejected')
    return render(request, "student_detail.html", {"student": student,"enrollments": enrollments,"accepted" : accepted,"pending":pending,"rejected":rejected})

@principal_required 
def add_addon_course(request):
    if request.method == "POST":
        form = AddOnCourseForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully.")
            return redirect("addon_course_list")

    else:
        form = AddOnCourseForm()

    return render(request, "add_addon_course.html", {"form": form})

@principal_required 
def addon_course_list(request):
    courses = AddOnCourse.objects.all()
    return render(request, "addon_course_list.html", {"courses": courses})

def delete_course(request, id):
    """Delete a course and all its enrollments"""
    course = get_object_or_404(AddOnCourse, id=id)
    course_name = course.course_name
    course.delete()
    
    messages.success(request, f"Course '{course_name}' deleted successfully!")
    return redirect("addon_course_list")

@principal_required 
def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully.")
            return redirect("principal_dashboard")

    else:
        form = DepartmentForm()

    return render(request, "add_department.html", {"form": form})

def approve_enrollment(request, enrollment_id):
    """Approve a pending enrollment"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if enrollment.status == 'pending':
        enrollment.status = 'accepted'
        enrollment.save()
        messages.success(request, f"Enrollment for {enrollment.student.user.username} in {enrollment.course.course_name} approved!")
    else:
        messages.warning(request, "This enrollment has already been processed.")
    
    return redirect('principal_dashboard')

def reject_enrollment(request, enrollment_id):
    """Reject a pending enrollment"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if enrollment.status == 'pending':
        enrollment.status = 'rejected'
        enrollment.save()
        messages.success(request, f"Enrollment for {enrollment.student.user.username} in {enrollment.course.course_name} rejected.")
    else:
        messages.warning(request, "This enrollment has already been processed.")
    
    return redirect('principal_dashboard')