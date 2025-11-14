from django.urls import path
from .views import RegisterView, LoginView, TokenRefreshView,GoogleLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
]
