from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/login/', views.Login.as_view(), name='login'),  # Use your custom Login view
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('notes/', views.notes, name='notes'),
    path('info/', views.user_info, name='info'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/dashboard/', views.admin_dashboard, name='dashboard'),
    # Comment out or remove the line below if using the custom Login view
    #path('accounts/login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)