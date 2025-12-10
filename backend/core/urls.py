from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomerViewSet, LeadSourceViewSet, LeadViewSet,
    ProposalViewSet, ProjectViewSet,
    SalesRegionViewSet, RegionSalesStatViewSet,
    TaskViewSet,
    SectionCategoryViewSet, SectionViewSet,
    CardViewSet, ExpenseCategoryViewSet,
    TransactionViewSet, ScheduledPaymentViewSet,
    ExchangeRateViewSet, VisitorStatViewSet,
    dashboard_summary,
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'lead-sources', LeadSourceViewSet)
router.register(r'leads', LeadViewSet)