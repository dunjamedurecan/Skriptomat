from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, PostViewSet
from .paypal_views import create_paypal_order, capture_paypal_order, paypal_webhook

router = DefaultRouter()
router.register(r"documents", DocumentViewSet, basename="document")
router.register(r"documents-feed", PostViewSet, basename="posts-feed")

urlpatterns = router.urls + [
    path('paypal/create-order/', create_paypal_order, name='paypal-create-order'),
    path('paypal/capture-order/', capture_paypal_order, name='paypal-capture-order'),
    path('paypal/webhook/', paypal_webhook, name='paypal-webhook'),
]