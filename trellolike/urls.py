"""trellolike URL Configuration

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
from django.urls import path, include
from rest_framework import routers

from myboard.API.api_views import TaskViewSet, TaskStatusViewSet, UserViewSet
from myboard.views import LoginUser, Index, Logout, Register, CreateTask, UpdateAssign, UpdateDescription, DeleteCard, \
    UpdateStatus

router = routers.DefaultRouter()
router.register(r'task_api', TaskViewSet, basename='task')
router.register(r'status_api', TaskStatusViewSet, basename='status')
router.register(r'user_api', UserViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginUser.as_view(), name='login'),
    path('', Index.as_view(), name='index'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('new/', CreateTask.as_view(), name='new'),
    path('assign/<int:pk>/', UpdateAssign.as_view(), name='assign_update'),
    path('task_update/<int:pk>/', UpdateDescription.as_view(), name='task_update'),
    path('task_delete/<int:pk>/', DeleteCard.as_view(), name='task_delete'),
    path('status/<int:pk>/', UpdateStatus.as_view(), name='status_update'),
    path('', include(router.urls)),
]
urlpatterns += [
    path('api_auth/', include('rest_framework.urls')),
]