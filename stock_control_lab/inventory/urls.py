from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProdutoListCreateView, ProdutoRetrieveUpdateDestroyView,
    StockLotListCreateView, StockLotRetrieveUpdateDestroyView, MovimentacaoEstoqueListCreateView,
    RequisitionListCreateView, RequisitionApproveRejectView,
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    SupplierListCreateView, SupplierRetrieveUpdateDestroyView,
    LocationListCreateView, LocationRetrieveUpdateDestroyView,
    AttachmentListCreateView, AttachmentRetrieveUpdateDestroyView,
    AuditLogListCreateView, AuditLogRetrieveUpdateDestroyView,
    UserListCreateView, UserRetrieveUpdateDestroyView,
    DashboardSummaryView, FinancialReportView,
    ProdutoListView, ProdutoDetailView, RequisitionListView, DashboardView, StockLotCreateView, MovimentacaoEstoqueWithdrawView,
    ConsumptionByUserReportView, WasteLossReportView, StockValueReportView, ExpiryReportView,
    ProdutoViewSet, MovimentacaoEstoqueViewSet, StockLotViewSet, CategoryViewSet, SupplierViewSet,
    LocationViewSet, AttachmentViewSet, AuditLogViewSet, RequisitionViewSet
)

# Create router and register ViewSets
router = DefaultRouter()
router.register(r'produtos-viewset', ProdutoViewSet, basename='produto')
router.register(r'movimentacoes-viewset', MovimentacaoEstoqueViewSet, basename='movimentacao')
router.register(r'stock-lots-viewset', StockLotViewSet, basename='stocklot')
router.register(r'categories-viewset', CategoryViewSet, basename='category')
router.register(r'suppliers-viewset', SupplierViewSet, basename='supplier')
router.register(r'locations-viewset', LocationViewSet, basename='location')
router.register(r'attachments-viewset', AttachmentViewSet, basename='attachment')
router.register(r'audit-logs-viewset', AuditLogViewSet, basename='auditlog')
router.register(r'requisitions-viewset', RequisitionViewSet, basename='requisition')

urlpatterns = [
    # Generic API views (for backwards compatibility)
    path('produtos/', ProdutoListCreateView.as_view(), name='produto-list-create'),
    path('produtos/<int:pk>/', ProdutoRetrieveUpdateDestroyView.as_view(), name='produto-detail'),
    
    path('stock-lots/', StockLotListCreateView.as_view(), name='stocklot-list-create'),
    path('stock-lots/<int:pk>/', StockLotRetrieveUpdateDestroyView.as_view(), name='stocklot-detail'),
    path('movimentacoes/', MovimentacaoEstoqueListCreateView.as_view(), name='movimentacao-list-create'),

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
    path('produtos/list/', ProdutoListView.as_view(), name='produto-list'),
    path('produtos/<int:pk>/detail/', ProdutoDetailView.as_view(), name='produto-detail-view'),
    path('requisitions/list/', RequisitionListView.as_view(), name='requisition-list'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('stock-lots/create/', StockLotCreateView.as_view(), name='stocklot-create'),
    path('movimentacoes/withdraw/', MovimentacaoEstoqueWithdrawView.as_view(), name='movimentacao-withdraw'),

    # Report URLs
    path('reports/consumption-by-user/', ConsumptionByUserReportView.as_view(), name='consumption-by-user-report'),
    path('reports/waste-loss/', WasteLossReportView.as_view(), name='waste-loss-report'),
    path('reports/stock-value/', StockValueReportView.as_view(), name='stock-value-report'),
    path('reports/expiry/', ExpiryReportView.as_view(), name='expiry-report'),

    # ViewSet URLs
    path('viewsets/', include(router.urls)),
]