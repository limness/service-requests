
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='user_register'),
    path('auth/', jwt_views.TokenObtainPairView.as_view(), name='auth_token'),
    path('auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('register_car/', views.RegisterCarView.as_view(), name='car_register'),
    path('expert_list/', views.ExpertsListView.as_view(), name='list_experts'),
    path('update_name/<int:pk>/', views.UpdateNameView.as_view(), name='update_name'),
    path('update_car/<int:pk>/', views.UpdateCarView.as_view(), name='update_car'),
]
