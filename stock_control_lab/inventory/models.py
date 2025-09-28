from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from inventory.utils import CustomJsonEncoder, generate_qr_code_image # Import generate_qr_code_image

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    fornecedor = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    data_validade = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nome

class StockLot(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    lot_number = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    expiry_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('produto', 'lot_number')

    def __str__(self):
        return f'{self.produto.nome} - Lote: {self.lot_number}'

    def get_qr_code_image(self):
        # For simplicity, encode the lot ID. In a real app, this might be a URL to the lot's detail page.
        return generate_qr_code_image(str(self.id))

class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saida'),
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.tipo} de {self.quantidade} no {self.produto.nome}'

class Attachment(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    file = models.FileField(upload_to='attachments/')
    description = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Anexo para {self.produto.nome} - {self.description}'

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True, encoder=CustomJsonEncoder)

    def __str__(self):
        return f'{self.user} - {self.action} em {self.timestamp}'

class Requisition(models.Model):
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Aprovada', 'Aprovada'),
        ('Rejeitada', 'Rejeitada'),
    )
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requisitions')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requisitions')
    request_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Requisição de {self.produto.nome} por {self.requester.username}'

class Alert(models.Model):
    ALERT_TYPE_CHOICES = (
        ('low_stock', 'Estoque Baixo'),
        ('expiry_date', 'Data de Validade'),
    )
    name = models.CharField(max_length=100)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor de referência para o alerta (ex: quantidade mínima, dias para expirar)")
    users_to_notify = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='alerts_to_notify')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta '{self.name}' para {self.produto.nome}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.user.username}: {self.message[:50]}"
