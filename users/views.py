from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.constants import (
    FILTER_INTERESTED_IN_MY,
    FILTER_OWNERS_OF_FAVORITES,
    FILTER_OWNERS_OF_PARTICIPATING,
    FILTER_PARTICIPANTS_OF_MY,
    MSG_PASSWORD_CHANGED,
    MSG_PROFILE_UPDATED,
    MSG_WELCOME,
    USERS_PER_PAGE,
)
from team_finder.utils import paginate
from users.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    ProfileEditForm,
    RegistrationForm,
)
from users.models import User


def register(request):
    form = RegistrationForm(request.POST or None) if request.method == 'POST' else RegistrationForm()
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:project_list')

    form = AuthenticationForm(request.POST or None) if request.method == 'POST' else AuthenticationForm()
    if request.method == 'POST' and form.is_valid():
        login(request, form.user)
        next_url = request.GET.get('next', '/projects/list/')
        return redirect(next_url)
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:project_list')


def profile_view(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    projects = profile_user.owned_projects.all()
    page_obj = paginate(projects, request, USERS_PER_PAGE)

    return render(request, 'users/user-details.html', {
        'user': profile_user,
        'projects': page_obj,
    })


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, MSG_PROFILE_UPDATED)
            return redirect('users:user_detail', user_id=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, MSG_PASSWORD_CHANGED)
            return redirect('users:user_detail', user_id=request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


def participants_view(request):
    participants = User.objects.filter(is_active=True)
    active_filter = request.GET.get('filter', '')

    if not request.user.is_authenticated or not active_filter:
        page_obj = paginate(participants, request, USERS_PER_PAGE)
        return render(request, 'users/participants.html', {
            'participants': page_obj,
            'active_filter': active_filter,
        })

    if active_filter == FILTER_OWNERS_OF_FAVORITES:
        participants = participants.filter(
            owned_projects__in=request.user.favorites.all()
        )
    elif active_filter == FILTER_OWNERS_OF_PARTICIPATING:
        participants = participants.filter(
            owned_projects__in=request.user.participated_projects.all()
        )
    elif active_filter == FILTER_INTERESTED_IN_MY:
        participants = participants.filter(
            favorites__in=request.user.owned_projects.all()
        )
    elif active_filter == FILTER_PARTICIPANTS_OF_MY:
        participants = participants.filter(
            participated_projects__in=request.user.owned_projects.all()
        ).exclude(id=request.user.id)

    participants = participants.distinct()
    page_obj = paginate(participants, request, USERS_PER_PAGE)

    return render(request, 'users/participants.html', {
        'participants': page_obj,
        'active_filter': active_filter,
    })