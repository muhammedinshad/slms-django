from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    dept_name = models.CharField(max_length=50)
    dept_description = models.TextField()

    def __str__(self):
        return self.dept_name
    
class AddOnCourse(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=50)
    course_description = models.TextField()
    course_price = models.IntegerField()

    def __str__(self):
        return self.course_name
    
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('AddOnCourse', on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'course']  # Prevent duplicate enrollments
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.course.course_name} ({self.status})"