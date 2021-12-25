from django.urls import path

from . import views

# Add a namespace

app_name = 'theora'

urlpatterns = [
    path('', views.theora_front, name='theora_front'),
    # path('post/<int:post_id>/', views.post_details, name='post_details'),
    # path('newpost/', views.newpost, name='newpost'),
    path('welcome/(?P<username>\w+)/$', views.welcome, name='welcome'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]