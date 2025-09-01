from django.db import models

class SyncCursor(models.Model):
    """Stores ISO8601 timestamp of last successful incremental sync."""
    key = models.CharField(max_length=64, unique=True)  # e.g. "tickets_updated_since"
    value = models.CharField(max_length=64)

class TicketCache(models.Model):
    """Lightweight local cache for quick UI/search; Freshdesk remains SoR."""
    ticket_id = models.BigIntegerField(unique=True)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=64)
    priority = models.CharField(max_length=64, null=True, blank=True)
    requester_id = models.BigIntegerField(null=True, blank=True)
    company_id = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    tags = models.JSONField(default=list)

class ContactCache(models.Model):
    contact_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

class WebhookEvent(models.Model):
    """Idempotency + audit for webhook deliveries from Freshdesk automations."""
    received_at = models.DateTimeField(auto_now_add=True)
    ticket_id = models.BigIntegerField(null=True, blank=True)
    event = models.CharField(max_length=128)  # e.g., 'ticket.created', 'ticket.updated'
    payload_hash = models.CharField(max_length=64)  # sha256 for dedupe
    raw = models.JSONField()
    class Meta:
        indexes = [
            models.Index(fields=["ticket_id", "event"]),
            models.Index(fields=["payload_hash"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["payload_hash"], name="uniq_fd_payload_hash")
        ]
