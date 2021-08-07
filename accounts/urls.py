from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('edit', views.user_edit, name='edit'),
    path('change_password', views.change_password, name='change_password'),
    path('activate/<uuid:token>', views.activate_user, name='activate'),
]