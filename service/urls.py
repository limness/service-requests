
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterUserView.as_view(), name='user_register'),
    path('auth/', jwt_views.TokenObtainPairView.as_view(), name='auth_token'),
    path('auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('register_car/', views.RegisterCar.as_view(), name='hello'),
]
