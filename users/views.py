from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import User
from .forms import RegistrationForm, LoginForm, EditProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = 12

    def get_queryset(self):
        return User.objects.all().order_by('id')


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('users:login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                return redirect('projects:projects')
            else:
                form.add_error(None, 'Неверный имейл или пароль')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:projects')


@login_required
def profile_change_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:participant_detail', pk=user.pk)
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def password_change_view(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('projects:projects')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'users/change_password.html', {'form': form})