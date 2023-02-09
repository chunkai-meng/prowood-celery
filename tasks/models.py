from django.urls import reverse
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import Group

from common.utils import MediaFileSystemStorage


# from .tasks import mass_send, sms_send


#
# class Category(models.Model):
#     name = models.CharField('Name', max_length=80, unique=True)
#     description = models.TextField(
#         'Description', max_length=255, blank=True, null=True)
#
#     class Meta:
#         ordering = ['name']
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'
#
#     def __str__(self):
#         return self.name
#
#
# class Template(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=64, default="")
#     description = models.TextField(default="")
#     subject = models.CharField(max_length=512, blank=True)
#     text_body = models.TextField(blank=True)
#     html_body = models.TextField(blank=True)
#
#     def __str__(self):
#         return f"{self.category} - {self.name}"


# class BaseNotification(models.Model):
#     email_from = models.EmailField(blank=True)
#     email_to = models.EmailField(blank=True)
#     sms_to = models.CharField(max_length=16, blank=True, help_text="Phone number")
#     sms = models.CharField(max_length=160, blank=True, help_text="SMS text")
#     email_task_id = models.CharField(max_length=128, blank=True)
#     sms_task_id = models.CharField(max_length=128, blank=True)
#
#     class Meta:
#         abstract = True
#         ordering = ['-id']


# class Notification(BaseNotification):
#     task_sn = models.CharField(max_length=64, blank=True, null=True)
#     template = models.ForeignKey(Template, on_delete=models.PROTECT)
#     subject_value1 = models.CharField(max_length=1024, blank=True)
#     subject_value2 = models.CharField(max_length=1024, blank=True)
#     subject_value3 = models.CharField(max_length=1024, blank=True)
#     subject_value4 = models.CharField(max_length=1024, blank=True)
#     body_value1 = models.CharField(max_length=2048, blank=True)
#     body_value2 = models.CharField(max_length=2048, blank=True)
#     body_value3 = models.CharField(max_length=2048, blank=True)
#     body_value4 = models.CharField(max_length=2048, blank=True)
#     body_value5 = models.CharField(max_length=2048, blank=True)
#     body_value6 = models.CharField(max_length=2048, blank=True)
#     send_at = models.DateTimeField(blank=True, null=True)
#     revoked = models.BooleanField(default=False)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["task_sn", "email_to", "send_at"],
#                 name="unique_sn_email_send_at",
#             )
#         ]
#
#     def __str__(self):
#         return self.template and self.template.category.name or "No Template"
#
#     @property
#     def subject(self):
#         return self.template.subject.format(
#             self.subject_value1,
#             self.subject_value2,
#             self.subject_value3,
#             self.subject_value4,
#         )
#
#     @property
#     def text_body(self):
#         return self.template.text_body.format(
#             self.body_value1,
#             self.body_value2,
#             self.body_value3,
#             self.body_value4,
#             self.body_value5,
#             self.body_value6,
#         )
#
#     @property
#     def html_body(self):
#         return self.template.html_body.format(
#             self.body_value1,
#             self.body_value2,
#             self.body_value3,
#             self.body_value4,
#             self.body_value5,
#             self.body_value6,
#         )
#
#     def save(self, *args, **kwargs):
#         if self.revoked:
#             super().save(*args, **kwargs)
#             return
#
#         self.sms_to = self.sms_to.replace(" ", "").replace("-", "")
#         if self.send_at:
#             now = timezone.now()
#             countdown = (self.send_at - now).total_seconds()
#             email_result = mass_send.apply_async(
#                 (self.task_sn, self.email_from, self.email_to, self.subject, self.text_body, self.html_body),
#                 link=None, countdown=countdown)
#             if self.sms_to and self.sms:
#                 sms_result = sms_send.apply_async((self.task_sn, self.sms_to, self.sms), link=None, countdown=countdown)
#         else:
#             email_result = mass_send.delay(
#                 self.task_sn, self.email_from, self.email_to, self.subject, self.text_body, self.html_body
#             )
#             if self.sms_to and self.sms:
#                 sms_result = sms_send.delay(self.task_sn, self.sms_to, self.sms)
#         self.email_task_id = email_result.task_id
#         self.sms_task_id = sms_result.task_id
#         super().save(*args, **kwargs)


class Email(models.Model):
    email_from = models.CharField(max_length=128)
    email_to = ArrayField(models.EmailField(max_length=512), help_text="e.g. abc@email.co,xyz@gmail.com")
    subject = models.CharField(max_length=128)
    text_content = models.TextField()
    html_content = models.TextField()
    token = models.CharField(max_length=128, blank=True)
    attachment = models.FileField('File', upload_to='files', max_length=256, storage=MediaFileSystemStorage(),
                                  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("email-detail", args=[str(self.pk)])
