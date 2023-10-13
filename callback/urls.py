from django.urls import path
from . import views

urlpatterns = [
    path('', views.callback),
    path('update_server/', views.update_server, name='update_server'),
]
