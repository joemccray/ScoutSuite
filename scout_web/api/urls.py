from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .drf import views as drf_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'cloudproviders', views.CloudProviderViewSet, basename='cloudprovider')
router.register(r'accounts', views.AccountViewSet, basename='account')
router.register(r'scans', views.ScanViewSet, basename='scan')
router.register(r'findings', views.FindingViewSet, basename='finding')
router.register(r'rulesets', views.RuleSetViewSet, basename='ruleset')
router.register(r'rules', views.RuleViewSet, basename='rule')
router.register(r'exceptions', views.RuleExceptionViewSet, basename='exception')
router.register(r"agents", drf_views.AgentsViewSet, basename="agents")
router.register(r"workflows", drf_views.WorkflowsViewSet, basename="workflows")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
