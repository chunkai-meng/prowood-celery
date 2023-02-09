import json
from datetime import datetime
from celery import Celery
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.conf import settings
from .tasks import mass_send, email_on_success
from .forms import EmailForm
from django.views.generic import View, CreateView, DetailView
from .models import Email
from django.shortcuts import render, redirect
from .decorators import source_ip_control

celery_app = Celery('app', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BROKER_URL)


class EmailDetailView(DetailView):
    model = Email


class EmailCreateView(CreateView):
    model = Email
    fields = '__all__'

    def form_valid(self, form):
        response = super().form_valid(form)
        mass_send.delay(
            self.object.task_sn,
            1,
            self.object.email_from,
            self.object.email_to,
            self.object.subject,
            self.object.text_content,
            self.object.html_content
        )
        return response


class EmailFormView(View):
    form_class = EmailForm
    initial = {'token': '$s0xzks2iy*wo*3y'}
    template_name = 'email_task/email_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('email-detail', pk=obj.id)

        return render(request, self.template_name, {'form': form})


# class EmailNotificationCreateView(CreateAPIView):
#     queryset = Notification.objects.all()
#     serializer_class = EmailNotificationSerializer
#     # permission_classes = (CheckApiKeySign, CheckSourceIP)


@csrf_exempt
@require_http_methods(["POST"])
@source_ip_control
def celery_email(request):
    response_data = {"message": "", "data": {}}
    if request.POST.get('token', None):
        data = request.POST
    else:
        data = json.loads(request.body.decode("utf-8"))

    if data.get('token') == settings.CELERY_API_KEY:
        task_sn = data.get('task_sn', '')
        callback = data.get('callback')
        email_from = data.get('from') or ''
        email_to = data.get('to')
        subject = data.get('subject') or ''
        text_content = data.get('text_content')
        html_content = data.get('html_content')
        send_at = data.get('send_at', '')
        countdown = data.get('countdown', 0)

        if send_at:
            send_at_datetime = datetime.strptime(send_at, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            countdown = (send_at_datetime - now).total_seconds()
            response_data["message"] = f"send_at: {send_at}"

        if callback or send_at or countdown:
            link = callback and email_on_success.s() or None
            result = mass_send.apply_async(
                (task_sn, email_from, email_to, subject, text_content, html_content, callback),
                link=link, countdown=countdown)
            response_data["data"] = {"task_id": str(result), "countdown": countdown}
        else:
            result = mass_send.delay(task_sn, email_from, email_to, subject,
                                     text_content, html_content)
            response_data["data"] = {"task_id": str(result)}
    else:
        response_data["message"] = str(request.POST.get('token')) + ': token not correct'

    return JsonResponse(response_data)


class SendEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        callback = data.get('callback')
        email_from = data.get('from', '')
        email_to = data.get('to')
        subject = data.get('subject', '')
        text_content = data.get('text_content', '')
        html_content = data.get('html_content', '')
        task_sn = data.get('task_sn', '')
        if callback:
            # print('callback')
            result = mass_send.apply_async(
                (task_sn, email_from, email_to, subject, text_content, html_content, callback),
                link=email_on_success.s())
        else:
            # print('no callback')
            result = mass_send.delay(task_sn, email_from, email_to, subject,
                                     text_content, html_content, )

        msg = 'Task added to queue: ' + str(result)
        return JsonResponse({
            'message': 'OK',
            'code': 1,
            'data': msg}, status=200)


class OpenSMSAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.data.get('token') == settings.CELERY_API_KEY:
            sent_num = 0
            message = "OK"
            code = 1
            data = request.data.get('payload')
            tasks = {}
            if not isinstance(data, list):
                message = "request error: please post a list of phone number and text pair"
                code = 0
            else:
                for sms_data in data:
                    task_sn = sms_data.get('task_sn', '')
                    phone_number = sms_data.get('phone_number')
                    text = sms_data.get('text', '')
                    r = sms_send.delay(task_sn, phone_number, text)
                    tasks[phone_number] = str(r)
                    sent_num += 1
            return JsonResponse({
                'message': message,
                'code': code,
                'data': {"total sent": sent_num, "task id": tasks}}, status=200)
        else:
            return JsonResponse({
                'message': "token error",
                'code': 0,
                'data': {"total sent": 0, "task id": 0}}, status=200)

#
# @csrf_exempt
# @source_ip_control
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def revoke_task(request):
#     """
#     revoke task, revoke all task with the same task_sn and send_at
#     """
#     task_sn = request.data.get('task_sn')
#     email_to = request.data.get("email_to")
#     send_at = request.data.get('send_at')
#     if not task_sn or not send_at or not email_to:
#         return Response("request error: please post task_sn and send_at and email_to", status=400)
#
#     send_at = string_to_localtime(send_at)
#     queryset = Notification.objects.filter(task_sn=task_sn, send_at=send_at, email_to=email_to)
#     result = []
#     for n in queryset:
#         # app.control.revoke(n.email_task_id, terminate=True, signal='SIGKILL')
#         # app.control.revoke(n.sms_task_id, terminate=True, signal='SIGKILL')
#         # print("n.email_task_id", n.email_task_id)
#         # print("status:", TaskResult.objects.get_task(n.email_task_id).status)
#         # revoked = default_app.control.revoke(n.email_task_id, terminated=True, signal='SIGKILL')
#         # print(revoked)
#         # print("sms_task_id: ", n.sms_task_id)
#         # print("status:", TaskR
#         # result.objects.get_task(n.sms_task_id).status)
#         # revoked = default_app.control.revoke(n.sms_task_id, terminated=True, signal='SIGKILL')
#         # print(revoked)
#         celery_app.control.revoke(n.email_task_id, terminate=True)
#         celery_app.control.revoke(n.sms_task_id, terminate=True)
#         n.revoked = True
#         n.save(update_fields=['revoked'])
#         result += {"email task": f"{n.email_task_id}", "sms task": f"{n.sms_task_id}"}
#     else:
#         return Response({"revoked": result})
