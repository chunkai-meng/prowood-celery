from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from proj.routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls), name='api'),
    path('tasks/', include('tasks.urls')),
]
urlpatterns += staticfiles_urlpatterns()
