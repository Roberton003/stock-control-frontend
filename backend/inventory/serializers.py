from rest_framework import serializers
from .models import Reagent, StockLot, StockMovement, Category, Supplier, Location, Attachment, AuditLog, Requisition, User

class ReagentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reagent
        fields = '__all__'

class StockLotSerializer(serializers.ModelSerializer):
    qr_code_image = serializers.SerializerMethodField()

    class Meta:
        model = StockLot
        fields = [
            'id', 'reagent', 'lot_number', 'location', 'expiry_date',
            'purchase_price', 'initial_quantity', 'current_quantity',
            'entry_date', 'qr_code_image'
        ]

    def get_qr_code_image(self, obj):
        return obj.get_qr_code_image()

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ('id', 'stock_lot', 'user', 'quantity', 'move_type', 'timestamp', 'notes')

    def create(self, validated_data):
        stock_lot = validated_data.get('stock_lot')
        quantity = validated_data.get('quantity')
        move_type = validated_data.get('move_type')

        if move_type == 'Entrada':
            stock_lot.current_quantity += quantity
        elif move_type == 'Ajuste':
            stock_lot.current_quantity += quantity # Assuming quantity can be positive or negative for adjustment
        elif move_type == 'Descarte':
            stock_lot.current_quantity -= quantity
        stock_lot.save()

        return super().create(validated_data)

class StockWithdrawalSerializer(serializers.Serializer):
    stock_lot = serializers.PrimaryKeyRelatedField(queryset=StockLot.objects.all())
    reagent_id = serializers.IntegerField(write_only=True) # Mark as write_only
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    notes = serializers.CharField(allow_blank=True, required=False)

    def create(self, validated_data, user=None): # Accept user as a keyword argument
        reagent_id = validated_data.pop('reagent_id')
        quantity = validated_data.get('quantity')
        notes = validated_data.get('notes', '')
        # user = validated_data.pop('user') # Removed

        stock_lot = validated_data['stock_lot'] # Now it's the object

        if stock_lot.current_quantity < quantity:
            raise serializers.ValidationError("Insufficient stock in the selected lot.")

        # stock_lot.current_quantity -= quantity # Removed
        # stock_lot.save() # Removed

        stock_movement = StockMovement.objects.create(
            stock_lot=stock_lot,
            user=user,
            quantity=quantity,
            move_type='Retirada',
            notes=notes
        )
        return stock_movement



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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name')