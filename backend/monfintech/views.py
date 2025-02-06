import uuid
import requests
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from . models import Transaction, Budget, Payment
from . serializers import TransactionSerializer, BudgetSerializer, PaymentSerializer
from django.core.exceptions import ObjectDoesNotExist

class ModelPagination(LimitOffsetPagination):
    page_size = 10 # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    pagination_class = ModelPagination
    filterset_fields = ['category', 'date']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetListCreateView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		query = request.query_params.get('q', '')
		budgets = Budget.objects.filter(user=request.user)
		if query:
			budgets = budgets.filter(
				Q(budget_name__icontains=query) | Q(description__icontains=query)
			)
		paginator = ModelPagination()
		paginated_budgets = paginator.paginate_queryset(budgets, request)
		serializer = BudgetSerializer(budgets, many=True)
		return paginator.get_paginated_response(serializer.data)

	def post(self, request):
		serializer = BudgetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BudgetDetailView(APIView):
	permission_classes = [IsAuthenticated]

	def get_object(self, pk, user):
		try:
			return Budget.objects.get(pk=pk, user=user)
		except Budget.DoesNotExist:
			return None

	def put(self, request, pk):
		budget = self.get_object(pk, request.user)
		if not budget:
			return Response({"error": "Budget not found"}, status=status.HTTP_404_NOT_FOUND)

		serializer = BudgetSerializer(budget, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		budget = self.get_object(pk, request.user)
		if not budget:
			return Response({"error": "Budget not found not authorized"}, status=status.HTTP_403_FORBIDDEN)

		budget.delete()
		return Response({"message": "Budget deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PaymentView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		data = request.data
		data['user'] = request.user.id
		data['transaction_id'] = uuid.uuid4().hex[:1] # unique transaction id
		#Validate the request
		serializer = PaymentSerializer(data=data)
		if serializer.is_valid():
			payment = serializer.save()

			# Process payment based on the method
			if data['payment_method'] == 'crypto':
				response = self.process_crypto(payment)
			elif data['payment_method'] == 'card':
				response = self.process_mastercard(payment)
			elif data['payment_method'] == 'mobile_money':
				response = self.process_mobile_money(payment)
			else:
				return Response({"error": "Invalid payment method"}, status=status.HTTP_400_BAD_REQUEST)

			# Update payment status
			payment.status = 'successful' if response.get('success') else 'failed'
			payment.gateway_response = response
			payment.save()

			return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def process_crypto(self, payment):
		# Add a cryptocurrency API URL here
		response = requests.post('https://api.crypto.com/payments', json={
			'amount': float(payment.amount),
			'recipient_wallet': payment.recipient,
			'transaction_id': payment.transaction_id,
		})
		return response.json()

	def process_mastercard(self, payment):
		# Add Mastercard API URL here
		response = requests.post('https://api.mastercard.com/payments', json={
			'amount': float(payment.amount),
			'card_number': payment.recipient, # Enter card number here
			'transaction_id': payment.transaction_id,
		})
		return response.json()

	def process_mobile_money(self, payment):
		# Add MTN, Telecel or AirtelTigo API URLs here
		response = requests.post('https://api.paystack.co/transfer', json={
			'amount': float(payment.amount),
			'recipient': payment.recipient,
			'reference': payment.transaction_id,
		}, headers={
			'Authorization': 'Bearer YOUR_API_KEY',
			'Content-Type': 'application/json'
		})
		return response.json()