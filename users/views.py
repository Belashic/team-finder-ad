from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import User
from .forms import RegistrationForm, AuthenticationForm, ProfileEditForm, PasswordChangeForm
from team_finder.constants import (
    USERS_PER_PAGE,
    FILTER_OWNERS_OF_FAVORITES,
    FILTER_OWNERS_OF_PARTICIPATING,
    FILTER_INTERESTED_IN_MY,
    FILTER_PARTICIPANTS_OF_MY,
)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('users:login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:project_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            next_url = request.GET.get('next', '/projects/list/')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:project_list')


def profile_view(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    projects = profile_user.owned_projects.all().order_by('-created_at')
    
    paginator = Paginator(projects, USERS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
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
            return redirect('users:user_detail', user_id=request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})


def participants_view(request):
    participants = User.objects.filter(is_active=True).order_by('id')
    active_filter = request.GET.get('filter', '')

    if request.user.is_authenticated and active_filter:
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

    paginator = Paginator(participants, USERS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/participants.html', {
        'participants': page_obj,
        'active_filter': active_filter,
    })