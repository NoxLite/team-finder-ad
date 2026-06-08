from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

class GitHubURLCleanerMixin:
    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        
        if not github_url:
            return github_url
        
        validator = URLValidator()
        try:
            validator(github_url)
        except ValidationError:
            raise forms.ValidationError('Введите корректную ссылку на GitHub')
        
    
        if not github_url.startswith('https://github.com/'):
            raise forms.ValidationError('Ссылка на GitHub должна начинаться с https://github.com/')
        
        return github_url
