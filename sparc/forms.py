from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Role choices
ROLE_CHOICES = [
    ('Sales Agent', 'Sales Agent'),
    ('Sales Supervisor', 'Sales Supervisor'),
    ('Sales Manager', 'Sales Manager'),
]

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Select Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash password
        if commit:
            user.save()
            Profile.objects.create(user=user, role=self.cleaned_data["role"])  # Create Profile
        return user
