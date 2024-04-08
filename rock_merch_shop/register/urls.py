from django.urls import path
from .views import register, profile, contact
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='register/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile, name='profile'),
    path('contact/', contact, name='contact')
    # other paths...
]