from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('crypto/', include('crypto.urls')),
    path('admin/', admin.site.urls),
]