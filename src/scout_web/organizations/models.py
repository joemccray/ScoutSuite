from django.conf import settings
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

class OrgRole(models.Model):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    ROLES = [(OWNER, "Owner"), (ADMIN, "Admin"), (MEMBER, "Member")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="roles")
    role = models.CharField(max_length=16, choices=ROLES)
    class Meta:
        unique_together = (("user", "organization"),)
