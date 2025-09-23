import datetime
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView, DetailView
from django.db.models import Sum, F, Q
from django.db.models.functions import TruncMonth
from decimal import Decimal

from .models import Reagent, StockLot, StockMovement, Requisition, Category, Supplier, Location, Attachment, AuditLog, User
from .serializers import ReagentSerializer, StockLotSerializer, StockMovementSerializer, StockWithdrawalSerializer, RequisitionSerializer, CategorySerializer, SupplierSerializer, LocationSerializer, AttachmentSerializer, AuditLogSerializer, UserSerializer
from .services import approve_requisition, calculate_total_stock_value


# Frontend Views
class ReagentListView(TemplateView):
    template_name = 'reagents/list_create.html'

class ReagentDetailView(DetailView):
    model = Reagent
    template_name = 'reagents/detail.html'
    context_object_name = 'reagent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related stock lots and attachments to the context
        context['stock_lots'] = self.object.stocklot_set.all()
        context['attachments'] = self.object.attachments.all()
        return context

class RequisitionListView(TemplateView):
    template_name = 'requisitions/list_create.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class StockLotCreateView(TemplateView):
    template_name = 'stock_lots/create_form.html'

class StockMovementWithdrawView(TemplateView):
    template_name = 'stock_movements/withdraw_form.html'


# API Views

class ObtainAuthToken(APIView):
    """
    API view to obtain a user authentication token.
    """
    permission_classes = [] # No permissions for login

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class Logout(APIView):
    """
    API view to logout a user.
    """
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReagentListCreateView(generics.ListCreateAPIView):
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer

class ReagentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer

class StockLotListCreateView(generics.ListCreateAPIView):
    queryset = StockLot.objects.all()
    serializer_class = StockLotSerializer

class StockLotRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockLot.objects.all()
    serializer_class = StockLotSerializer

class StockMovementListCreateView(generics.ListCreateAPIView):
    queryset = StockMovement.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' and self.request.data.get('move_type') == 'Retirada':
            return StockWithdrawalSerializer
        return StockMovementSerializer

    def perform_create(self, serializer):
        # The serializer's create method will handle the actual creation and stock updates
        # We just need to pass the user from the request
        serializer.save(user=self.request.user, stock_lot=serializer.validated_data['stock_lot'])

class RequisitionListCreateView(generics.ListCreateAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer

class RequisitionApproveRejectView(APIView):
    def post(self, request, pk, format=None):
        try:
            requisition = Requisition.objects.get(pk=pk)
        except Requisition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')

        if action == 'approve':
            try:
                approve_requisition(requisition, request.user)
                serializer = RequisitionSerializer(requisition)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif action == 'reject':
            requisition.status = 'Rejeitada'
            requisition.approver = request.user
            requisition.approval_date = datetime.datetime.now()
            requisition.save()
            serializer = RequisitionSerializer(requisition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

# CRUD Views for other models
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class AttachmentListCreateView(generics.ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class AttachmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class AuditLogListCreateView(generics.ListCreateAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

class AuditLogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Dashboard and Reports Views
class DashboardSummaryView(APIView):
    def get(self, request, format=None):
        # Total Stock Value
        total_stock_value = calculate_total_stock_value()

        # Low Stock Items
        low_stock_items = Reagent.objects.filter(min_stock_level__gt=0).annotate(
            current_total_stock=Sum('stocklot__current_quantity')
        ).filter(Q(current_total_stock__lt=F('min_stock_level')) | Q(current_total_stock__isnull=True))
        low_stock_items_data = [{'name': item.name, 'sku': item.sku, 'current_stock': item.current_total_stock or 0, 'min_stock': item.min_stock_level} for item in low_stock_items]

        # Expiring Soon Items (e.g., next 90 days)
        ninety_days_from_now = datetime.date.today() + datetime.timedelta(days=90)
        expiring_soon_items = StockLot.objects.filter(
            expiry_date__lte=ninety_days_from_now,
            expiry_date__gte=datetime.date.today(),
            current_quantity__gt=0
        ).select_related('reagent')
        expiring_soon_items_data = [{'reagent': item.reagent.name, 'lot_number': item.lot_number, 'expiry_date': item.expiry_date, 'quantity': item.current_quantity} for item in expiring_soon_items]

        # Consumption Data (last 6 months)
        today = datetime.date.today()
        six_months_ago = today - datetime.timedelta(days=180)
        consumption_data_raw = StockMovement.objects.filter(
            move_type='Retirada',
            timestamp__gte=six_months_ago
        ).annotate(
            month=TruncMonth('timestamp')
        ).values('month').annotate(total_quantity=Sum('quantity')).order_by('month')

        consumption_labels = [data['month'].strftime('%Y-%m') for data in consumption_data_raw]
        consumption_values = [float(data['total_quantity']) for data in consumption_data_raw]

        # Expiry Data (pie chart categories)
        expired_count = StockLot.objects.filter(expiry_date__lt=datetime.date.today(), current_quantity__gt=0).count()
        expiring_soon_count = StockLot.objects.filter(
            expiry_date__gte=datetime.date.today(),
            expiry_date__lte=ninety_days_from_now,
            current_quantity__gt=0
        ).count()
        valid_count = StockLot.objects.filter(expiry_date__gt=ninety_days_from_now, current_quantity__gt=0).count()

        expiry_labels = ['Vencidos', 'Vencem em 90 dias', 'Válidos']
        expiry_values = [expired_count, expiring_soon_count, valid_count]

        data = {
            'total_stock_value': total_stock_value,
            'low_stock_items': low_stock_items_data,
            'expiring_soon_items': expiring_soon_items_data,
            'consumption_data': {'labels': consumption_labels, 'values': consumption_values},
            'expiry_data': {'labels': expiry_labels, 'values': expiry_values}
        }
        return Response(data, status=status.HTTP_200_OK)

class FinancialReportView(APIView):
    def get(self, request, format=None):
        # Placeholder for financial report logic
        data = {
            'total_spent': 0.0,
            'period': ''
        }
        return Response(data, status=status.HTTP_200_OK)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ReagentViewSet(viewsets.ModelViewSet):
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer


class StockLotViewSet(viewsets.ModelViewSet):
    queryset = StockLot.objects.all()
    serializer_class = StockLotSerializer


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

    @action(detail=False, methods=['post'], url_path='withdraw')
    def withdraw(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reagent_id = serializer.validated_data.get('reagent_id')
        quantity = serializer.validated_data.get('quantity')
        notes = serializer.validated_data.get('notes', '')

        reagent = get_object_or_404(Reagent, pk=reagent_id)
        user = request.user  # Assuming user is authenticated

        try:
            with transaction.atomic():
                total_withdrawn = perform_withdrawal(reagent, quantity, user)
                # Create a single StockMovement record for the withdrawal
                # This might need adjustment if you want a movement per lot
                # For simplicity, we'll assume perform_withdrawal handles individual lot movements
                # and we just need a summary here if desired.
                # StockMovement.objects.create(reagent=reagent, user=user, quantity=total_withdrawn, move_type='Retirada', notes=notes)

            return Response({'status': 'withdrawal successful', 'total_withdrawn': total_withdrawn}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer


class RequisitionViewSet(viewsets.ModelViewSet):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        requisition = self.get_object()
        approver_user = request.user  # Assuming approver is authenticated

        try:
            approve_requisition(requisition, approver_user)
            return Response({'status': 'requisition approved'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        requisition = self.get_object()
        if requisition.status != 'Pendente':
            return Response({'error': 'Requisition is not in pending status.'}, status=status.HTTP_400_BAD_REQUEST)
        
        requisition.status = 'Rejeitada'
        requisition.approver = request.user
        requisition.approval_date = timezone.now()
        requisition.save()
        return Response({'status': 'requisition rejected'}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .services import (
    get_consumption_by_user_report,
    get_waste_loss_report,
    get_stock_value_report,
    get_expiry_report
)

class ConsumptionByUserReportView(APIView):
    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        user_id = request.query_params.get('user_id')
        reagent_id = request.query_params.get('reagent_id')

        if not start_date_str or not end_date_str:
            return Response({"error": "start_date and end_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Date format should be YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        report_data = get_consumption_by_user_report(
            start_date, end_date,
            user_id=user_id,
            reagent_id=reagent_id
        )
        return Response(report_data, status=status.HTTP_200_OK)

class WasteLossReportView(APIView):
    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        reagent_id = request.query_params.get('reagent_id')

        if not start_date_str or not end_date_str:
            return Response({"error": "start_date and end_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Date format should be YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        report_data = get_waste_loss_report(
            start_date, end_date,
            reagent_id=reagent_id
        )
        return Response(report_data, status=status.HTTP_200_OK)

class StockValueReportView(APIView):
    def get(self, request, *args, **kwargs):
        group_by = request.query_params.get('group_by')

        try:
            report_data = get_stock_value_report(group_by=group_by)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(report_data, status=status.HTTP_200_OK)

class ExpiryReportView(APIView):
    def get(self, request, *args, **kwargs):
        days_until_expiry_str = request.query_params.get('days_until_expiry')
        expired_str = request.query_params.get('expired')

        days_until_expiry = None
        if days_until_expiry_str:
            try:
                days_until_expiry = int(days_until_expiry_str)
            except ValueError:
                return Response({"error": "days_until_expiry must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        
        expired = expired_str and expired_str.lower() == 'true'

        report_data = get_expiry_report(
            days_until_expiry=days_until_expiry,
            expired=expired
        )
        return Response(report_data, status=status.HTTP_200_OK)