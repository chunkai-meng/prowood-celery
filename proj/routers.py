from rest_framework import routers

from tasks.viewsets import EmailViewSet

router = routers.DefaultRouter()

router.register(r'create-email', EmailViewSet, basename='create-email')
