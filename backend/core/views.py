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
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only current user's cards
        return Card.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)