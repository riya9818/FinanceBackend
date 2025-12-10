from datetime import timedelta
from django.shortcuts import render

# Create your views here.
from django.db.models import Sum, Q
from django.utils.timezone import now
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import (
    Customer, LeadSource, Lead, Proposal, Project,
    SalesRegion, RegionSalesStat, Task,
    SectionCategory, Section,
    Card, ExpenseCategory, Transaction, ScheduledPayment,
    ExchangeRate, VisitorStat
)
from .serializers import (
    CustomerSerializer, LeadSourceSerializer, LeadSerializer,
    ProposalSerializer, ProjectSerializer,
    SalesRegionSerializer, RegionSalesStatSerializer,
    TaskSerializer, SectionCategorySerializer, SectionSerializer,
    CardSerializer, ExpenseCategorySerializer, TransactionSerializer,
    ScheduledPaymentSerializer, ExchangeRateSerializer,
    VisitorStatSerializer
)


# --------- GENERIC VIEWSETS (CRUD) ---------

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-joined_date')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeadSourceViewSet(viewsets.ModelViewSet):
    queryset = LeadSource.objects.all()
    serializer_class = LeadSourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all().order_by('-sent_date')
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-start_date')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class SalesRegionViewSet(viewsets.ModelViewSet):
    queryset = SalesRegion.objects.all()
    serializer_class = SalesRegionSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegionSalesStatViewSet(viewsets.ModelViewSet):
    queryset = RegionSalesStat.objects.all()
    serializer_class = RegionSalesStatSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class SectionCategoryViewSet(viewsets.ModelViewSet):
    queryset = SectionCategory.objects.all()
    serializer_class = SectionCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by('order_index')
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only current user's cards
        return Card.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # all transactions for current user's cards
        return Transaction.objects.filter(card__user=self.request.user).order_by('-transaction_date')

class ScheduledPaymentViewSet(viewsets.ModelViewSet):
    queryset = ScheduledPayment.objects.all()
    serializer_class = ScheduledPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScheduledPayment.objects.filter(card__user=self.request.user).order_by('due_date')

class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class VisitorStatViewSet(viewsets.ModelViewSet):
    queryset = VisitorStat.objects.all().order_by('date')
    serializer_class = VisitorStatSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary(request):
    """
    Returns the numbers for the main dashboard cards:
    - total_revenue
    - new_customers (last 30 days)
    - active_accounts (active customers)
    - growth_rate 
    """
    user = request.user
    today = now().date()
    last_30_days = today - timedelta(days=30)

    transactions = Transaction.objects.filter(card__user=user)
    total_revenue = transactions.filter(amount__gt=0).aggregate(
        total=Sum("amount")
    )["total"] or 0

#customer card logic to filter in dashboard page
    new_customers = Customer.objects.filter(joined_date__gte=last_30_days).count()
    active_accounts = Customer.objects.filter(is_active=True).count()

    growth_rate = 0

    return Response({
        "total_revenue": total_revenue,
        "new_customers": new_customers,
        "active_accounts": active_accounts,
        "growth_rate": growth_rate,
    })