from rest_framework import serializers, viewsets, routers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TicketCache
from .services import create_ticket, add_public_reply

class TicketCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCache
        fields = ["ticket_id", "subject", "status", "priority", "requester_id", "company_id", "tags", "created_at", "updated_at"]

class TicketsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketCache.objects.all().order_by("-updated_at")
    serializer_class = TicketCacheSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["post"], detail=False, url_path="create")
    def create_ticket(self, request):
        data = request.data
        ticket = create_ticket(
            subject=data["subject"],
            email=data["email"],
            description=data.get("description", ""),
            tags=data.get("tags", []),
            attachments=data.get("attachments", []),
        )
        return Response({"ticket_id": ticket.id, "subject": ticket.subject})

    @action(methods=["post"], detail=True, url_path="reply")
    def reply(self, request, pk=None):
        body = request.data["body"]
        add_public_reply(int(pk), body)
        return Response({"ok": True})

router = routers.DefaultRouter()
router.register(r"tickets", TicketsViewSet, basename="tickets")
