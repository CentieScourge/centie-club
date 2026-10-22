from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils import timezone


class Business(models.Model):
    TYPE_CHOICES = [
        ('СТО', 'СТО'),
        ('Клуб', 'Клуб'),
        ('Ресторан/Кафе', 'Ресторан/Кафе'),
        ('Остальное', 'Остальное'),
    ]
    STATUS_CHOICES = [
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
        ('pending', 'В обработке'),
    ]
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Остальное')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='free')
    price = models.CharField(max_length=100)
    image = models.ImageField(upload_to='businesses/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Альтернатива загрузке файла')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Бизнес'
        verbose_name_plural = 'Бизнесы'

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)
    photo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    history = HistoricalRecords()

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    image = models.ImageField(upload_to='documents/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    google_doc_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.title


class Review(models.Model):
    name = models.CharField(max_length=200, default='Гражданин LS')
    text = models.TextField()
    answer = models.TextField(blank=True)
    answer_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.name} — {self.created_at:%Y-%m-%d}'


class Meeting(models.Model):
    STATUS_CHOICES = [
        ('inwork', 'В работе'),
        ('accepted', 'Принято'),
        ('finished', 'Закончена'),
    ]
    TOPIC_CHOICES = [
        ('Бизнес-вопрос', 'Бизнес-вопрос'),
        ('Жалоба', 'Жалоба на действия госслужащих'),
        ('Земля/недвижимость', 'Вопрос по недвижимости'),
        ('Законодательство', 'Вопрос по законодательству'),
        ('Встреча для мероприятия', 'Встреча для мероприятия'),
        ('Другое', 'Другое'),
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    card_id = models.CharField(max_length=50)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    custom_topic = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inwork')
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка на приём'
        verbose_name_plural = 'Заявки на приём'

    def __str__(self):
        return f'{self.name} — {self.topic}'


class PrivateOrg(models.Model):
    name = models.CharField(max_length=200)
    founder = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        verbose_name = 'Частная организация'
        verbose_name_plural = 'Частные организации'

    def __str__(self):
        return self.name


class SiteInfo(models.Model):
    key = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField(help_text='HTML разрешён')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Информационный блок'
        verbose_name_plural = 'Информационные блоки'

    def __str__(self):
        return self.title


class AuditLog(models.Model):
    """Simple explicit audit log in addition to simple_history."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Запись аудита'
        verbose_name_plural = 'Журнал аудита'

    def __str__(self):
        return f'{self.timestamp:%Y-%m-%d %H:%M} {self.user} {self.action} {self.model_name}'


class Notification(models.Model):
    """Live notifications for active admin sessions."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.title
