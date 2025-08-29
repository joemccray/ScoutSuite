import time
from datetime import datetime, timezone
from typing import Optional

import requests
from celery import shared_task
from django.conf import settings
from django.db import transaction
from prometheus_client import Counter, Histogram

from .models import SyncCursor, TicketCache, ContactCache
from .services import list_tickets, get_ticket, get_contact

SYNC_RUNS = Counter("freshdesk_sync_runs_total", "Total Freshdesk sync runs")
SYNC_ERRORS = Counter("freshdesk_sync_errors_total", "Total Freshdesk sync errors")
RATE_LIMIT_HITS = Counter("freshdesk_rate_limit_hits_total", "HTTP 429s when calling Freshdesk")
WEBHOOK_PROCESS_TIME = Histogram("freshdesk_webhook_seconds", "Webhook processing time")

def _get_cursor(key: str, default_iso: str) -> str:
    obj, _ = SyncCursor.objects.get_or_create(key=key, defaults={"value": default_iso})
    return obj.value

def _set_cursor(key: str, iso: str) -> None:
    SyncCursor.objects.update_or_create(key=key, defaults={"value": iso})

def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def _respect_rate_limit(call_count: int, window_started: float, max_per_min: int):
    """Simple local limiter: ensure we don't exceed our plan per minute cap."""
    elapsed = time.time() - window_started
    if call_count >= max_per_min and elapsed < 60:
        time.sleep(60 - elapsed)

@shared_task(bind=True, max_retries=5)
def sync_tickets(self):
    SYNC_RUNS.inc()
    call_count = 0
    window_started = time.time()
    updated_since = _get_cursor("tickets_updated_since", default_iso="2014-01-01T00:00:00.000Z")
    page = 1
    while True:
        try:
            _respect_rate_limit(call_count, window_started, settings.FRESHDESK_MAX_CALLS_PER_MIN)
            tickets = list_tickets(updated_since_iso=updated_since, page=page, per_page=100)
            call_count += 1
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                RATE_LIMIT_HITS.inc()
                retry_after = int(e.response.headers.get("Retry-After", "60"))
                time.sleep(retry_after)
                continue
            SYNC_ERRORS.inc()
            raise

        if not tickets:
            break

        for t in tickets:
            with transaction.atomic():
                TicketCache.objects.update_or_create(
                    ticket_id=t.id,
                    defaults=dict(
                        subject=getattr(t, "subject", "") or "",
                        status=str(getattr(t, "status", "")),
                        priority=str(getattr(t, "priority", "")),
                        requester_id=getattr(t, "requester_id", None),
                        company_id=getattr(t, "company_id", None),
                        created_at=getattr(t, "created_at", None),
                        updated_at=getattr(t, "updated_at", None),
                        tags=list(getattr(t, "tags", []) or []),
                    ),
                )
                # Warm contact cache opportunistically
                rid = getattr(t, "requester_id", None)
                if rid:
                    try:
                        _respect_rate_limit(call_count, window_started, settings.FRESHDESK_MAX_CALLS_PER_MIN)
                        c = get_contact(rid)
                        call_count += 1
                        ContactCache.objects.update_or_create(
                            contact_id=c.id,
                            defaults=dict(
                                name=getattr(c, "name", "") or "",
                                email=getattr(c, "email", None),
                                phone=getattr(c, "phone", None),
                                updated_at=getattr(c, "updated_at", None),
                            ),
                        )
                    except Exception:
                        # Don't fail the whole sync on a contact miss
                        pass

        page += 1

    _set_cursor("tickets_updated_since", _iso_now())
    return "ok"
