from django.urls import path
from .views import RegisterView, LoginView, TokenRefreshView,GoogleLoginView,GoogleRegisterView,UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('googleregister/',GoogleRegisterView.as_view(),name='google_register'),
    path('profile/<str:username>/', UserProfileView.as_view(),name='user_profile'),
]
