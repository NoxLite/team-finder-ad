from django import forms
from django.contrib.auth import get_user_model 
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            return phone

        if not (phone.startswith('+7') or phone.startswith('8')):
            raise forms.ValidationError('Номер телефона должен начинаться с +7 или 8')

        if phone.startswith('8'):
            phone = '+7' + phone[1:]

        qs = User.objects.filter(phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот номер телефона уже используется')

        return phone
    
    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')

        if not github_url:
            return github_url
        
        if not github_url.startswith('https://github.com/'):
            raise forms.ValidationError('Ссылка на GitHub должна начинаться с https://github.com/')
        
        validator = URLValidator()
        try:
            validator(github_url)
        except ValidationError:
            raise forms.ValidationError('Введите корректную ссылку на GitHub')
        
        return github_url

    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
