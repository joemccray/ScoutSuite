from django.db import models
from scout_web.organizations.models import Organization

class CloudProvider(models.Model):
    """
    Represents a cloud provider supported by ScoutSuite.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)  # e.g., 'aws', 'azure', 'gcp'

    class Meta:
        unique_together = (('organization', 'name'), ('organization', 'code'))

    def __str__(self):
        return self.name

class Account(models.Model):
    """
    Represents a cloud account to be scanned.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(CloudProvider, on_delete=models.CASCADE)
    credentials = models.JSONField()  # Store credentials in an encrypted way in a real app
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Scan(models.Model):
    """
    Represents a single scan run.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    configuration = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Scan for {self.account.name} at {self.created_at}"

class Finding(models.Model):
    """
    Represents a single finding from a scan.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE)
    rule_name = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=50) # e.g., 'danger', 'warning'
    raw_finding = models.JSONField() # The raw JSON from the scout report
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule_name

class RuleSet(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('organization', 'name'),)

    def __str__(self):
        return self.name

class Rule(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    ruleset = models.ForeignKey(RuleSet, on_delete=models.CASCADE, related_name='rules')
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    # Other rule properties can be added here

    def __str__(self):
        return self.name

class RuleException(models.Model):
    # An exception to a rule for a specific resource
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    resource_id = models.CharField(max_length=255)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exception for {self.rule.name} on {self.resource_id}"
