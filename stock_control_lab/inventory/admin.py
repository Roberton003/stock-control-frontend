from django.contrib import admin
from .models import User, Category, Supplier, Location, Produto, StockLot, MovimentacaoEstoque, Alert, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sku', 'category', 'fornecedor', 'quantidade')
    list_filter = ('category', 'fornecedor')
    search_fields = ('nome', 'sku')

@admin.register(StockLot)
class StockLotAdmin(admin.ModelAdmin):
    list_display = ('produto', 'lot_number', 'location', 'current_quantity', 'expiry_date')
    list_filter = ('location', 'expiry_date')
    search_fields = ('produto__nome', 'lot_number')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('name', 'produto', 'alert_type', 'threshold_value', 'is_active')
    list_filter = ('alert_type', 'is_active')
    search_fields = ('name', 'produto__nome')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'user')
    search_fields = ('message',)

# Register other models with default admin
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Location)
admin.site.register(MovimentacaoEstoque)