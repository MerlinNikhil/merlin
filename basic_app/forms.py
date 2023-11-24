from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_protect


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')

class LoginForm(AuthenticationForm):
    # Additional login form fields or customization if needed
    class Meta:
        model = User # Replace YourUserModel with your actual User model
        fields = ['username', 'password']
