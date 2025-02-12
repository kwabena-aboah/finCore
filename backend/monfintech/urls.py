from django.urls import path
from . views import TransactionListCreateView, BudgetListCreateView, BudgetDetailView, PaymentView

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
    path('payments/', PaymentView.as_view(), name='payment-view'),
]