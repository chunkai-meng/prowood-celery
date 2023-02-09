from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

from .tasks import mass_send
from .serializers import EmailSerializer
from .models import Email


class EmailViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        obj = serializer.instance
        result = mass_send.delay(1, obj.email_from, obj.email_to, obj.subject,
                                 obj.text_content, obj.html_content)
        return JsonResponse(
            {
                'message': 'OK',
                'code': 1,
                'data': 'Task added to queue: ' + str(result)
            },
            status=200
        )
