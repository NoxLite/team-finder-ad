from django.contrib import admin

from .models import Project, Skill


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'github_url',
        'status',
        'owner',
        'created_at'     
    )
    list_filter = (
        'status',
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
