from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from basic_app.forms import UserForm, UserProfileInfoForm
from basic_app.models import UserProfileInfo

def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('basic_app:index')
                else:
                    print("User account is not active.")
    else:
        login_form = AuthenticationForm()

    return render(request, 'basic_app/login.html', {'login_form': login_form})


@login_required
def special(request):
     user_profile, created  = UserProfileInfo.objects.get_or_create(user=request.user)

     return render(request, 'basic_app/special.html', {'user_profile': user_profile, 'created': created})


@login_required
def user_logout(request):
    logout(request)
    return redirect('basic_app:index')
