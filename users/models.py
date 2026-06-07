from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

import constants
from .managers import generate_avatar, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    name = models.CharField(max_length=constants.LEN_NAME_USER, verbose_name="Имя")
    surname = models.CharField(max_length=constants.LEN_SURNAME, verbose_name="Фамилия")
    
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Аватарка")
    phone = models.CharField(max_length=constants.LEN_PHONE, verbose_name="Номер телефона")
    
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    about = models.TextField(max_length=constants.LEN_ABOUT, blank=True, verbose_name="Описание профиля")
    
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    objects = UserManager()
 
    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar = generate_avatar(self.name[0], number_of_user=User.objects.count())
        super().save(*args, **kwargs)
