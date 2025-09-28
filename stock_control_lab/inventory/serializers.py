from rest_framework import serializers
from .models import Produto, StockLot, MovimentacaoEstoque, Category, Supplier, Location, Attachment, AuditLog, Requisition, User, Alert, Notification
from .services import perform_withdrawal
from decimal import Decimal

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'password', 'date_joined', 'is_active')
        read_only_fields = ('date_joined', 'is_active')
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class StockLotSerializer(serializers.ModelSerializer):
    qr_code_image = serializers.SerializerMethodField()

    class Meta:
        model = StockLot
        fields = [
            'id', 'produto', 'lot_number', 'location', 'expiry_date',
            'purchase_price', 'initial_quantity', 'current_quantity',
            'entry_date', 'qr_code_image'
        ]

    def get_qr_code_image(self, obj):
        return obj.get_qr_code_image()

class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentacaoEstoque
        fields = ('id', 'produto', 'usuario', 'quantidade', 'tipo', 'data')
        read_only_fields = ('data',)

    def create(self, validated_data):
        movimentacao = super().create(validated_data)
        # Atualiza a quantidade no produto baseado na movimentação
        produto = movimentacao.produto
        if movimentacao.tipo == 'ENTRADA':
            produto.quantidade += movimentacao.quantidade
        elif movimentacao.tipo == 'SAIDA':
            produto.quantidade -= movimentacao.quantidade
        produto.save()
        
        return movimentacao

class StockWithdrawalSerializer(serializers.Serializer):
    produto_id = serializers.IntegerField(required=True)
    quantidade = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    notes = serializers.CharField(allow_blank=True, required=False)

    def create(self, validated_data):
        produto_id = validated_data.get('produto_id')
        quantidade = validated_data.get('quantidade')
        notes = validated_data.get('notes', '')
        user = self.context['request'].user

        try:
            produto = Produto.objects.get(id=produto_id)
            total_withdrawn = perform_withdrawal(produto, quantidade, user)
            
            # Criar um registro de movimentação de estoque para o saque
            MovimentacaoEstoque.objects.create(
                produto=produto,
                usuario=user,
                quantidade=total_withdrawn,
                tipo='SAIDA',
                notes=notes
            )
            
            return validated_data
        except Produto.DoesNotExist:
            raise serializers.ValidationError({"produto_id": "Produto não encontrado."})
        except ValueError as e:
            raise serializers.ValidationError({"non_field_errors": [str(e)]})

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class RequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = '__all__'
        read_only_fields = ('request_date', 'approval_date')

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'