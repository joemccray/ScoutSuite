from django.urls import path, include
from .api import router
from .webhooks import freshdesk_webhook

urlpatterns = [
    path("api/", include(router.urls)),
    path("webhook/", freshdesk_webhook, name="freshdesk-webhook"),
]
