import json
import http

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

import constants
from .forms import CreateProjectForm
from .models import Project, Skill


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = constants.PAGINATE_BY

    def get_queryset(self):
        ParticipantModel = Project._meta.get_field('participants').related_model

        qs = (
            Project.objects
            .select_related('owner')
            .prefetch_related(
                'skills',
                Prefetch(
                    'participants',
                    queryset=ParticipantModel.objects.only('id'),
                    to_attr='prefetched_participants'
                )
            )
            .order_by('-created_at')
        )
        
        skill = self.request.GET.get('skill', '').strip()
        if skill:
            qs = qs.filter(skills__name__iexact=skill).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for project in context['projects']:
            project.participants_count = len(project.prefetched_participants)
            
        skill_name = self.request.GET.get('skill', '').strip()
        context['all_skills'] = Skill.objects.all().order_by('name')
        context['active_skill'] = Skill.objects.filter(name__iexact=skill_name).first() if skill_name else None
        
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'


@login_required
def create_project(request):
    form = CreateProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        form.save_m2m()
        project.participants.add(request.user)
        return redirect('projects:project_detail', pk=project.pk)
    
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.user != project.owner:
        return http.HttpResponseForbidden('Forbidden')
    
    form = CreateProjectForm(request.POST or None, instance=project)
    
    if form.is_valid():
        form.save()
        return redirect('projects:project_detail', pk=project.pk)
    
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


@login_required
def close_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.user != project.owner:
        return http.HttpResponseForbidden('Forbidden')
    
    project.status = constants.PROJECT_STATUS_CLOSE
    project.save()
    return http.HTTPStatus.OK


def get_skills(request):
    q = request.GET.get('q', '')
    skills = (
        Skill.objects
        .filter(name__istartswith=q)
        .order_by('name')
        .values('id', 'name')[:constants.COUNT_SKILLS]
    )
    return JsonResponse(list(skills), safe=False)


@require_POST
@login_required
def add_skill(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner != request.user:
        return http.HTTPStatus.FORBIDDEN

    data = json.loads(request.body)
    skill_id = data.get('skill_id')
    name = data.get('name')

    created = False

    if skill_id:
        skill = Skill.objects.get(pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return http.HTTPStatus.BAD_REQUEST

    added = not project.skills.filter(pk=skill.pk).exists()
    if added:
        project.skills.add(skill)

    return JsonResponse({
        'id': skill.pk,
        'name': skill.name,
        'created': created,
        'added': added,
    })


@login_required
def toggle_participation(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner == request.user:
        return http.HTTPStatus.FORBIDDEN
    
    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({
        'status': 'ok',
        'participant': not is_participant,
    })


@login_required
def remove_skill(request, pk, skill_id):
    project = get_object_or_404(Project, pk=pk)
    
    if project.owner != request.user:
        return http.HTTPStatus.FORBIDDEN

    skill = Skill.objects.get(pk=skill_id)
    project.skills.remove(skill)

    return http.HTTPStatus.OK
