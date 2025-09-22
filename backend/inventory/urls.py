from django.urls import path
from .views import (
    ReagentListCreateView, ReagentRetrieveUpdateDestroyView,
    StockLotListCreateView, StockMovementListCreateView,
    RequisitionListCreateView, RequisitionApproveRejectView,
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    SupplierListCreateView, SupplierRetrieveUpdateDestroyView,
    LocationListCreateView, LocationRetrieveUpdateDestroyView,
    AttachmentListCreateView, AttachmentRetrieveUpdateDestroyView,
    AuditLogListCreateView, AuditLogRetrieveUpdateDestroyView,
    UserListCreateView, UserRetrieveUpdateDestroyView,
    DashboardSummaryView, FinancialReportView,
    ReagentListView, ReagentDetailView, RequisitionListView, DashboardView, StockLotCreateView, StockMovementWithdrawView,
    ConsumptionByUserReportView, WasteLossReportView, StockValueReportView, ExpiryReportView
)

urlpatterns = [
    path('reagents/', ReagentListCreateView.as_view(), name='reagent-list-create'),
    path('reagents/<int:pk>/', ReagentRetrieveUpdateDestroyView.as_view(), name='reagent-detail'),

    path('stock-lots/', StockLotListCreateView.as_view(), name='stocklot-list-create'),
    path('stock-movements/', StockMovementListCreateView.as_view(), name='stockmovement-list-create'),

    path('requisitions/', RequisitionListCreateView.as_view(), name='requisition-list-create'),
    path('requisitions/<int:pk>/action/', RequisitionApproveRejectView.as_view(), name='requisition-action'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('suppliers/', SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('suppliers/<int:pk>/', SupplierRetrieveUpdateDestroyView.as_view(), name='supplier-detail'),

    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationRetrieveUpdateDestroyView.as_view(), name='location-detail'),

    path('attachments/', AttachmentListCreateView.as_view(), name='attachment-list-create'),
    path('attachments/<int:pk>/', AttachmentRetrieveUpdateDestroyView.as_view(), name='attachment-detail'),

    path('audit-logs/', AuditLogListCreateView.as_view(), name='auditlog-list-create'),
    path('audit-logs/<int:pk>/', AuditLogRetrieveUpdateDestroyView.as_view(), name='auditlog-detail'),

    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),

    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('reports/financial/', FinancialReportView.as_view(), name='financial-report'),

    # Frontend URLs
    path('reagents/list/', ReagentListView.as_view(), name='reagent-list'),
    path('reagents/<int:pk>/detail/', ReagentDetailView.as_view(), name='reagent-detail-view'),
    path('requisitions/list/', RequisitionListView.as_view(), name='requisition-list'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('stock-lots/create/', StockLotCreateView.as_view(), name='stocklot-create'),
    path('stock-movements/withdraw/', StockMovementWithdrawView.as_view(), name='stockmovement-withdraw'),

    # Report URLs
    path('reports/consumption-by-user/', ConsumptionByUserReportView.as_view(), name='consumption-by-user-report'),
    path('reports/waste-loss/', WasteLossReportView.as_view(), name='waste-loss-report'),
    path('reports/stock-value/', StockValueReportView.as_view(), name='stock-value-report'),
    path('reports/expiry/', ExpiryReportView.as_view(), name='expiry-report'),
]