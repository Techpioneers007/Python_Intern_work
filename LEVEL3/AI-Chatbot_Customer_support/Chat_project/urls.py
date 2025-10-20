from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Panel (optional but standard)
    path('admin/', admin.site.urls),
    
    # REQUIRED: Maps all /api/ requests to the 'chat_app' routing file.
    path('api/', include('chat_app.urls')), 
]
