from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .models import Project
import constants

class CreateProjectForm(forms.ModelForm, constants.GitHubURLCleanerMixin):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
    
    
