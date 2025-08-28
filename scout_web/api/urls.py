from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'cloudproviders', views.CloudProviderViewSet, basename='cloudprovider')
router.register(r'accounts', views.AccountViewSet, basename='account')
router.register(r'scans', views.ScanViewSet, basename='scan')
router.register(r'findings', views.FindingViewSet, basename='finding')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
