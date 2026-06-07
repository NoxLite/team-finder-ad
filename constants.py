from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

LEN_NAME_PROJECT = 200
CHOICES_STATUS = [('open', 'Открытый'), ('closed', 'Закрытый')]
DEFAULT_PROJECT_STATUS = 'open'

LEN_NAME_SKILL = 124

PAGINATE_BY = 12

COUNT_SKILLS = 10

TEXT_COLOR = (255, 255, 255)
IMAGE_SIZE = 200
TEXT_SIZE = 0.6 * IMAGE_SIZE

LEN_NAME_USER = 124
LEN_SURNAME = 124
LEN_PHONE = 12
LEN_ABOUT = 256


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
