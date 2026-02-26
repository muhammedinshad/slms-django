from django import forms
from django.contrib.auth.models import User
from .models import Student

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Student
        exclude = ['user', 'role'] 
    def clean(self):
        """Validate password match"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def clean_username(self):
        """Validate username doesn't already exist"""
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        """Validate email doesn't already exist"""
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use another.")
        return email

    def clean_reg_number(self):
        """Validate registration number is unique"""
        reg_number = self.cleaned_data.get('reg_number')
        if Student.objects.filter(reg_number=reg_number).exists():
            raise forms.ValidationError("This registration number is already taken.")
        return reg_number

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'firstname',
            'lastname',
            'phone_number',
            'department',
            'profil'
        ]
