from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Business, Employee, News, Document, Review, Meeting,
    PrivateOrg, SiteInfo, AuditLog, Notification
)


@admin.register(Business)
class BusinessAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'type', 'status', 'price', 'created_at')
    list_filter = ('type', 'status')
    search_fields = ('name', 'address')
    list_editable = ('status',)


@admin.register(Employee)
class EmployeeAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'position', 'order')
    list_editable = ('order',)


@admin.register(News)
class NewsAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'published', 'created_at')
    list_filter = ('published',)
    search_fields = ('title', 'text')


@admin.register(Document)
class DocumentAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'text')


@admin.register(Review)
class ReviewAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'created_at', 'has_answer')
    search_fields = ('name', 'text', 'answer')

    def has_answer(self, obj):
        return bool(obj.answer)
    has_answer.boolean = True


@admin.register(Meeting)
class MeetingAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'topic', 'status', 'phone', 'created_at')
    list_filter = ('status', 'topic')
    list_editable = ('status',)
    search_fields = ('name', 'phone', 'card_id')


@admin.register(PrivateOrg)
class PrivateOrgAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'founder', 'phone', 'created_at')
    search_fields = ('name', 'founder')


@admin.register(SiteInfo)
class SiteInfoAdmin(SimpleHistoryAdmin):
    list_display = ('key', 'title')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'object_id')
    list_filter = ('action', 'model_name')
    search_fields = ('description', 'user__username')
    readonly_fields = ('timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('title', 'message')
