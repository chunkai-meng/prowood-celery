from django.urls import path
from .views import (
    celery_email, EmailCreateView, EmailDetailView, EmailFormView, SendEmail, OpenSMSAPI,
    # EmailNotificationCreateView, revoke_task,
)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', celery_email, name='token-free-mail'),
    # path('template-email/', csrf_exempt(EmailNotificationCreateView.as_view()), name='token-template-mail'),
    path('send-email/', csrf_exempt(SendEmail.as_view()), name='send-mail'),
    path('email-create/', EmailCreateView.as_view(), name='email-create'),
    path('open-sms-api/', csrf_exempt(OpenSMSAPI.as_view()), name='open-sms'),
    # path('revoke-task/', revoke_task, name='revoke-task'),
    path('<int:pk>/', EmailDetailView.as_view(), name='email-detail'),
    path('new/', EmailFormView.as_view())
]
