from django.contrib import admin
from .models import User, Category, Supplier, Location, Reagent, StockLot, StockMovement, Alert, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(Reagent)
class ReagentAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'supplier', 'min_stock_level')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'sku')

@admin.register(StockLot)
class StockLotAdmin(admin.ModelAdmin):
    list_display = ('reagent', 'lot_number', 'location', 'current_quantity', 'expiry_date')
    list_filter = ('location', 'expiry_date')
    search_fields = ('reagent__name', 'lot_number')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('name', 'reagent', 'alert_type', 'threshold_value', 'is_active')
    list_filter = ('alert_type', 'is_active')
    search_fields = ('name', 'reagent__name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'user')
    search_fields = ('message',)

# Register other models with default admin
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Location)
admin.site.register(StockMovement)