from django.urls import path

from . import views

# Add a namespace

app_name = 'asciichan'

urlpatterns = [
    path('', views.front, name='asciichan_front'),
]