from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .views import chatbot_response

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Courses & Enrollment
    path('courses/', views.courses, name='courses'),
    path('enroll/', views.enroll, name='enroll'),

    # Events & News
    path('events/', views.events, name='events'),
    path('event-register/', views.event_register, name='event-register'),
    path('news/', views.news, name='news'),

    # Profile & Contact
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('contact/', views.contact, name='contact'),

    # Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    # blog urls
    path('blog/ai-trends-2025/', views.ai_trends, name='ai-trends'),
    path('blog/fullstack-importance/', views.fullstack_blog, name='fullstack'),
    path('blog/cybersecurity-essentials/', views.cybersecurity_blog, name='cybersecurity'),

    # back home
    path('blog/', views.blog_home, name='blog_home'),  # New URL pattern for blog home
    path('blog/', views.blog_home, name='blog_home'),  # New URL pattern for blog home
    path('blog/', views.blog_home, name='blog_home'),  # New URL pattern for blog home
    path('', views.home, name='home'),

    #explore course  
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('enroll/', views.enroll, name='enroll'),
    path('enroll/<slug:slug>/', views.enroll_course, name='enroll_course'),
    path('chat/', chatbot_response, name='chatbot_response'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chat-api/', views.chat_api, name='chat_api')
    
]

# Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
