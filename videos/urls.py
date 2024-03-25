from django.urls import path
from . import views



# In videos/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.homepage, name='homepage'),  # Add this line
    path('upload/', views.upload_video, name='upload_video'),
    path('upload/success/', views.upload_video_success, name='video_upload_success'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('modify_video/<int:video_id>/', views.modify_video, name='modify_video'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)