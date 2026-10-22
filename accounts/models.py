from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('editor', 'Редактор'),
        ('viewer', 'Наблюдатель'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    phone = models.CharField(max_length=20, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_admin_role(self):
        return self.role in ('admin', 'editor') or self.is_superuser
