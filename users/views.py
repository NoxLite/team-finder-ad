from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from .forms import EditProfileForm, LoginForm, RegistrationForm
from .models import User

User = get_user_model()


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

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        return redirect('users:login')

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            login(request, user)
            return redirect('projects:projects')
        form.add_error(None, 'Неверный имейл или пароль')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:projects')


@login_required
def profile_change_view(request):
    user = request.user
    form = EditProfileForm(request.POST or None, request.FILES, instance=user)
    if form.is_valid():
        form.save()
        return redirect('users:participant_detail', pk=user.pk)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def password_change_view(request):
    user = request.user
    form = PasswordChangeForm(user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('projects:projects')

    return render(request, 'users/change_password.html', {'form': form})