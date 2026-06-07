from django.db import models
import io
import random
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

def generate_avatar(letter, number_of_user):
    is_lucky_user = random.choice([False, True]) #Если пользователь удачливый, то его фон будет в цвет Яндекса))))
    if is_lucky_user:
        r = 255
        g = 204
        b = 0
    else:
        r = random.randint(0, 110)
        g = random.randint(0, 110)
        b = random.randint(0, 110)
    background_color = (r, g, b)
    text_color = (255, 255, 255)
    
    img = Image.new('RGB', (200, 200), color=background_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except IOError:
        font = None
        
    letter = letter.upper()
    
    draw.text((100, 100), letter, fill=text_color, font=font, anchor="mm")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'avatar_{number_of_user}.png')


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email является обязательным полем')
        if not name or not surname:
            raise ValueError('Имя и Фамилия являются обязательными полями')
        if not phone:
            raise ValueError('Номер телефона является обязательным полем')

        email = self.normalize_email(email)
        
        extra_fields.setdefault('is_active', True)
        
        user = self.model(
            email=email,
            name=name,
            surname=surname,
            phone=phone,
            **extra_fields
        )
        
        if not user.avatar:
            
            user.avatar = generate_avatar(name[0], number_of_user=User.objects.count())

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff'):
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser'):
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, name, surname, phone, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    name = models.CharField(max_length=124, verbose_name="Имя")
    surname = models.CharField(max_length=124, verbose_name="Фамилия")
    
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Аватарка")
    phone = models.CharField(max_length=12, verbose_name="Номер телефона")
    
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    about = models.TextField(max_length=256, blank=True, verbose_name="Описание профиля")
    
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar = generate_avatar(self.name[0], number_of_user=User.objects.count())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
