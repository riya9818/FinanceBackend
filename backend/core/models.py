from django.db import models
from django.conf import settings
# Create your models here.

class Customer(models.Model):
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_customers'
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    joined_date = models.DateField()
    is_active = models.BooleanField(default=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
 
    
# CRM ENTITIES


class LeadSource(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
        
class Lead(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('qualified', 'Qualified'),
        ('proposal_sent', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )
    source = models.ForeignKey(
        LeadSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    created_at = models.DateTimeField(auto_now_add=True)
    expected_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Proposal(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='proposals'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proposals'
    )
    sent_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Proposal #{self.id} for {self.lead}"


class Project(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    proposal = models.OneToOneField(
        Proposal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='project'
    )
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    target_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    actual_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class SalesRegion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
