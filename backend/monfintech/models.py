import uuid
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - GHS{self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    budget_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.budget_name} - GHS {self.amount}"

def generate_unique_transaction_id():
    return str(uuid.uuid4().hex[:1])

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('crypto', 'Cryptocurrency'),
        ('card', 'Credit/Debit Card'),
        ('mobile_money', 'Mobile Money'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'failed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=20)
    recipient = models.CharField(max_length=255) # Crypto wallet, card number or phone number
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)
    transaction_id = models.CharField(max_length=100, unique=True, default=generate_unique_transaction_id)
    gateway_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - GHS{self.amount} - {self.status}"