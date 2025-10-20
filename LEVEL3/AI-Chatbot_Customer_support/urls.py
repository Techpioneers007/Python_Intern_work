# myproject/urls.py
from django.urls import path, include
# ...
urlpatterns = [
    # ...
    path('api/', include('chat_app.urls')), 
]