from django.urls import path
from .views import register, profile, contact
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # URL pattern for the registration page
    path('register/', register, name='register'),
    # URL pattern for the login page, utilizing Django's built-in LoginView
    path('login/', LoginView.as_view(template_name='register/login.html'), name='login'),
    # URL pattern for the logout process, utilizing Django's built-in LogoutView
    # Redirects to the login page after a successful logout
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # URL pattern for the user profile page
    path('profile/', profile, name='profile'),
    # URL pattern for the contact form page
    path('contact/', contact, name='contact')
]