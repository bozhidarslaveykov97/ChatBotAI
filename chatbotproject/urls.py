"""chatbotproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from chatbotweb import views
from rest_framework import routers

apiRouter = routers.DefaultRouter()
apiRouter.register('users', views.UserViewSet)
apiRouter.register('groups', views.GroupViewSet)

from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.index),

    path('api/', include(apiRouter.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

     # path('api/login', views.LoginView.as_view(), name='auth_register'),
    path('api/register', views.RegisterView.as_view(), name='auth_register'),

    path("api/send_chat", views.api_send_chat, name="api_send_chat"),
    path("api/get_random_question", views.api_get_random_question, name="api_get_random_question"),

    path('admin/', admin.site.urls)
]