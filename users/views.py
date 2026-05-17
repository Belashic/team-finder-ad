from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.constants import (
    FILTER_INTERESTED_IN_MY,
    FILTER_OWNERS_OF_FAVORITES,
    FILTER_OWNERS_OF_PARTICIPATING,
    FILTER_PARTICIPANTS_OF_MY,
    USERS_PER_PAGE,
)
from team_finder.utils import paginate

from .forms import AuthenticationForm, PasswordChangeForm, ProfileEditForm, RegistrationForm
from .models import User


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})
    
    form = RegistrationForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'users/register.html', {'form': form})
    
    user = form.save()
    return redirect('users:login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:project_list')
    
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})
    
    form = AuthenticationForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'users/login.html', {'form': form})
    
    login(request, form.user)
    next_url = request.GET.get('next', '/projects/list/')
    return redirect(next_url)


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
    if request.method == 'GET':
        form = ProfileEditForm(instance=request.user)
        return render(request, 'users/edit_profile.html', {'form': form})
    
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if not form.is_valid():
        return render(request, 'users/edit_profile.html', {'form': form})
    
    form.save()
    return redirect('users:user_detail', user_id=request.user.pk)


@login_required
def change_password_view(request):
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
        return render(request, 'users/change_password.html', {'form': form})
    
    form = PasswordChangeForm(request.user, request.POST or None)
    if not form.is_valid():
        return render(request, 'users/change_password.html', {'form': form})
    
    user = form.save()
    update_session_auth_hash(request, user)
    return redirect('users:user_detail', user_id=request.user.pk)


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