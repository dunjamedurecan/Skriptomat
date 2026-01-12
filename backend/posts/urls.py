from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, PostViewSet

router = DefaultRouter()
router.register(r"documents", DocumentViewSet, basename="document")
router.register(r"documents-feed", PostViewSet, basename="posts-feed")

urlpatterns = router.urls