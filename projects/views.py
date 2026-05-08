from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Project
from .forms import ProjectForm
from team_finder.constants import PROJECTS_PER_PAGE


def project_list(request):
    projects = Project.objects.select_related('owner').prefetch_related('participants').all()
    paginator = Paginator(projects, PROJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'projects/project_list.html', {'projects': page_obj})


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect('projects:project_detail', project_id=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', project_id=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if project.status == 'open':
        project.status = 'closed'
        project.save()
        return JsonResponse({'status': 'ok', 'project_status': 'closed'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.status == 'closed' and request.user not in project.participants.all():
        return JsonResponse({'status': 'error', 'message': 'Проект закрыт'}, status=400)
    if request.user in project.participants.all():
        project.participants.remove(request.user)
        return JsonResponse({'status': 'ok', 'participant': False})
    else:
        project.participants.add(request.user)
        return JsonResponse({'status': 'ok', 'participant': True})


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({'status': 'ok', 'favorited': favorited})


@login_required
def favorite_projects(request):
    projects = request.user.favorites.select_related('owner').prefetch_related('participants').all()
    paginator = Paginator(projects, PROJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'projects/favorite_projects.html', {'projects': page_obj})