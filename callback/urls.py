from django.urls import path
from . import views

urlpatterns = [
    path('', views.callback),
    path('line_login', views.line_login, name='Login'),
    path('line_callback', views.line_callback, name='callback'),
]
