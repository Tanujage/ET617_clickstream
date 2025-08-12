"""
URL configuration for ET617_clickstream project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from clickstream import views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.quiz_view, name='quiz_home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='accounts_login'),  # Add this line
    path('logout/', views.logout_view, name='logout'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('video/', views.video_view, name='video'),
    path('api/click/', views.collect_click_event, name='collect_click'),
]



