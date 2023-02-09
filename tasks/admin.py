from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import TextInput
from django.utils.html import mark_safe
from django.contrib.admin import register
from .models import Email


# Register your models here.
@register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject')
    formfield_overrides = {
        ArrayField: {'widget': TextInput(attrs={'size': '94'})},
        models.CharField: {'widget': TextInput(attrs={'size': '120'})},

    }
    fields = (
        'email_from', 'email_to', 'subject',
        'text_content', 'html_content', "preview", "created_at"
    )
    readonly_fields = ['preview']

    def has_change_permission(self, request, obj=None):
        return False

    def preview(self, obj):
        return mark_safe(obj.html_content)

    preview.short_description = 'Email Body Preview'

#
# @register(Notification)
# class EmailNotificationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'task_sn', 'template', 'subject', 'email_from', 'email_to', 'send_at', 'revoked')
#     fields = (
#         'preview', ('task_sn', 'revoked'),
#         'template', 'email_from', 'email_to', 'send_at',
#         'subject_value1', 'subject_value2', 'subject_value3', 'subject_value4',
#         'body_value1', 'body_value2', 'body_value3', 'body_value4', 'body_value5', 'body_value6',
#         'sms_to', 'sms', 'email_task_id', 'sms_task_id'
#     )
#     readonly_fields = ['preview']
#
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size': '120'})},
#     }
#
#     def preview(self, obj):
#         html_text = obj.template.html_body.format(
#             obj.body_value1,
#             obj.body_value2,
#             obj.body_value3,
#             obj.body_value4,
#             obj.body_value5,
#             obj.body_value6,
#         )
#         return mark_safe(html_text)
#
#
# @register(Template)
# class TemplateAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'category', 'subject')
#     fields = ('name', 'category', 'description', 'subject', 'text_body', 'html_body', 'body')
#     readonly_fields = ['body']
#
#     def body(self, obj):
#         return mark_safe(obj.html_body)
#
#
# @register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     pass
