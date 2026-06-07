from django.contrib import admin
from .models import Project, Skill


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


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill, SkillAdmin)