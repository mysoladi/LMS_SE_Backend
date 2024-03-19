"""
URL configuration for lms_login_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from lms_login_api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', CreateUserView.as_view(), name='create_user'),  # Endpoint for user registration
    path('login/', UserLoginView.as_view(), name='user_login'),    # Endpoint for user login
    path('recover-password/', PasswordRecoveryView.as_view(), name='password_recovery'),  # Endpoint for password recovery
    path('change-password/', ChangePasswordView.as_view(), name='sec_change_password'),
    path('email-password/', EmailPasswordRecoveryView.as_view(), name='email_change_password')
]

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns += router.urls
