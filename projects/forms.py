from django import forms

from mixins import GitHubURLCleanerMixin
from .models import Project

class CreateProjectForm(GitHubURLCleanerMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
