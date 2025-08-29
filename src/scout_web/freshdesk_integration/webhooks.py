import json
import time
from hashlib import sha256

from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

from .models import WebhookEvent, TicketCache

@csrf_exempt
def freshdesk_webhook(request):
    token = request.headers.get("X-FD-Webhook-Token")
    if token != settings.FRESHDESK_WEBHOOK_TOKEN:
        return HttpResponseForbidden("bad token")

    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("invalid json")

    # Make a stable hash for idempotency
    payload_hash = sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    evt, created = WebhookEvent.objects.get_or_create(
        payload_hash=payload_hash,
        defaults={
            "ticket_id": payload.get("ticket", {}).get("id") or payload.get("ticket_id"),
            "event": payload.get("event") or "ticket.updated",
            "raw": payload,
        },
    )
    if not created:
        return JsonResponse({"status": "duplicate"}, status=200)

    # Optional: update our cache immediately if useful fields exist
    t = payload.get("ticket") or {}
    if "id" in t:
        TicketCache.objects.update_or_create(
            ticket_id=int(t["id"]),
            defaults=dict(
                subject=t.get("subject") or "",
                status=str(t.get("status") or ""),
                priority=str(t.get("priority") or ""),
                requester_id=t.get("requester_id"),
                company_id=t.get("company_id"),
                # parse ISO strings safely
                created_at=parse_datetime(t.get("created_at")) if t.get("created_at") else None,
                updated_at=parse_datetime(t.get("updated_at")) if t.get("updated_at") else None,
                tags=t.get("tags") or [],
            ),
        )

    return JsonResponse({"ok": True})
