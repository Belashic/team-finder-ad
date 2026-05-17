from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from team_finder.constants import PROJECTS_PER_PAGE
from team_finder.utils import paginate

from .forms import ProjectForm
from .models import Project


def project_list(request):
    projects = Project.objects.select_related('owner').prefetch_related('participants')
    page_obj = paginate(projects, request, PROJECTS_PER_PAGE)
    return render(request, 'projects/project_list.html', {'projects': page_obj})


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project(request):
    if request.method == 'GET':
        form = ProjectForm()
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})
    
    form = ProjectForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})
    
    project = form.save(commit=False)
    project.owner = request.user
    project.save()
    project.participants.add(request.user)
    return redirect('projects:project_detail', project_id=project.pk)


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    
    if request.method == 'GET':
        form = ProjectForm(instance=project)
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})
    
    form = ProjectForm(request.POST or None, instance=project)
    if not form.is_valid():
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})
    
    form.save()
    return redirect('projects:project_detail', project_id=project.pk)


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    
    if project.status != 'open':
        return JsonResponse({'status': 'error'}, status=400)
    
    project.status = 'closed'
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': 'closed'})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if project.status == 'closed' and request.user not in project.participants.all():
        return JsonResponse({'status': 'error', 'message': 'Проект закрыт'}, status=400)
    
    if request.user in project.participants.all():
        project.participants.remove(request.user)
        return JsonResponse({'status': 'ok', 'participant': False})
    
    project.participants.add(request.user)
    return JsonResponse({'status': 'ok', 'participant': True})


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
        return JsonResponse({'status': 'ok', 'favorited': False})
    
    request.user.favorites.add(project)
    return JsonResponse({'status': 'ok', 'favorited': True})


@login_required
def favorite_projects(request):
    projects = request.user.favorites.select_related('owner').prefetch_related('participants')
    page_obj = paginate(projects, request, PROJECTS_PER_PAGE)
    return render(request, 'projects/favorite_projects.html', {'projects': page_obj})