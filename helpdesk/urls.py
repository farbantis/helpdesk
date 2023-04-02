from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('account.urls')),
    path('', include('tasks.urls')),
    path('api/account/', include('account.api.urls')),
    path('api/tasks/', include('tasks.api.urls')),
]
