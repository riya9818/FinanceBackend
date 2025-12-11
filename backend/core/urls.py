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
    dashboard_summary, finance_overview,
)

#router since auto generate 7 endpoints/urls of CRUD 
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'lead-sources', LeadSourceViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'sales-regions', SalesRegionViewSet)
router.register(r'region-sales', RegionSalesStatViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'section-categories', SectionCategoryViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'cards', CardViewSet)
router.register(r'expense-categories', ExpenseCategoryViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'scheduled-payments', ScheduledPaymentViewSet)
router.register(r'exchange-rates', ExchangeRateViewSet)
router.register(r'visitor-stats', VisitorStatViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/summary/', dashboard_summary, name='dashboard-summary'),
    path('finance/overview/', finance_overview, name='finance-overview')
]