import hashlib
from datetime import datetime, timezone
from typing import Dict, Iterable, Optional

from django.conf import settings
from freshdesk.api import API

def _client() -> API:
    proxies = None
    if settings.FRESHDESK_PROXY_HTTP or settings.FRESHDESK_PROXY_HTTPS:
        proxies = {
            "http": settings.FRESHDESK_PROXY_HTTP,
            "https": settings.FRESHDESK_PROXY_HTTPS,
        }
    return API(
        settings.FRESHDESK_DOMAIN,
        settings.FRESHDESK_API_KEY,
        version=2,
        verify=settings.FRESHDESK_VERIFY_SSL,
        proxies=proxies,
    )

def make_payload_hash(payload: Dict) -> str:
    return hashlib.sha256(str(payload).encode("utf-8")).hexdigest()

def create_ticket(subject: str, email: str, description: str, tags: Optional[Iterable[str]] = None, attachments: Optional[Iterable[str]] = None):
    a = _client()
    return a.tickets.create_ticket(
        subject,
        email=email,
        description=description,
        tags=list(tags or []),
        attachments=list(attachments or []),
    )

def add_public_reply(ticket_id: int, body: str):
    a = _client()
    return a.comments.create_reply(ticket_id, body)

def get_ticket(ticket_id: int, include: Iterable[str] = ()):
    a = _client()
    return a.tickets.get_ticket(ticket_id, *include)

def list_tickets(updated_since_iso: Optional[str] = None, page: Optional[int] = None, per_page: int = 100):
    a = _client()
    return a.tickets.list_tickets(updated_since=updated_since_iso, page=page, per_page=per_page)

def get_contact(contact_id: int):
    a = _client()
    return a.contacts.get_contact(contact_id)
