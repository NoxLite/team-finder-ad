from django.conf import settings
from django.db import models

import constants

class Project(models.Model):

    name = models.CharField(max_length=constants.LEN_NAME_PROJECT, verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание проекта")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_projects',
        verbose_name="Владелец проекта"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    status = models.CharField(
        max_length=constants.MAX_LEN_STATUS_PROJECT, 
        choices=constants.CHOICES_STATUS,           
        default=constants.DEFAULT_PROJECT_STATUS, 
        verbose_name="Статус проекта"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='participated_projects', 
        blank=True,
        verbose_name="Участники проекта"
    )
    skills = models.ManyToManyField('projects.Skill',
        related_name='projects', 
        blank=True,
        verbose_name='Навыки'
    )
    
    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self):
        return f"{self.name} {self.owner.name} ({self.status})"


class Skill(models.Model):
    name = models.CharField(max_length=constants.LEN_NAME_SKILL, unique=True)

    class Meta:
        verbose_name = "навык"
        verbose_name_plural = "Навыки"
    
    def __str__(self):
        return self.name
