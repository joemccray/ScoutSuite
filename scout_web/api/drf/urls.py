from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentsViewSet, WorkflowsViewSet

router = DefaultRouter()
router.register(r"agents", AgentsViewSet, basename="agents")
router.register(r"workflows", WorkflowsViewSet, basename="workflows")

urlpatterns = [path("", include(router.urls))]
