from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    TokenRefreshView, 
    GoogleLoginView, 
    GoogleRegisterView,
    GoogleRegistrationCompleteView,
    CurrentUserView,
    PublicUserProfileView,
    UserProfileView,
    CourseListView,
    FacultyListView,
    CourseSubscribeView,
    CourseUnsubscribeView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('googleregister/', GoogleRegisterView.as_view(), name='google_register'),
    path('googleregister/complete/', GoogleRegistrationCompleteView.as_view(), name='google_register_complete'),
    # User profile endpoints for Buy Me a Coffee feature
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('profile/<int:user_id>/', PublicUserProfileView.as_view(), name='public_profile'),
    # User profile view by username (from develop)
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    # Courses endpoint
    path('courses/', CourseListView.as_view(), name='courses'),
    # Faculties endpoint
    path('faculties/', FacultyListView.as_view(), name='faculties'),
    # Course subscription endpoints
    path('courses/<int:course_id>/subscribe/', CourseSubscribeView.as_view(), name='course_subscribe'),
    path('courses/<int:course_id>/unsubscribe/', CourseUnsubscribeView.as_view(), name='course_unsubscribe'),
]
