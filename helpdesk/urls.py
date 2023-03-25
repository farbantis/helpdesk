from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('account.urls')),
    path('', include('tasks.urls')),
]
