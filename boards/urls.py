from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('list_themes', views.list_themes, name='list_themes'),
    path('create_theme', views.create_theme, name='create_theme'),
]