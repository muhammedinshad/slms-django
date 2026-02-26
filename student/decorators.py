from functools import wraps
from django.shortcuts import redirect

def principal_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'student'):
            if request.user.student.role == "principal":
                return view_func(request, *args, **kwargs)
            else:
                # If student tries principal page
                return redirect("student_dashbord")
            
        return redirect("login")

    return wrapper

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'student'):
            if request.user.student.role == "student":
                return view_func(request, *args, **kwargs)
            else:
                # If principal tries student page
                return redirect("principal_dashboard")

        return redirect("login")

    return wrapper