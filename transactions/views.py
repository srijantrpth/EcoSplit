from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum,Q
from django.db.models.functions import Coalesce
from .models import Expense, Group, ExpenseSplit
import requests
from .serializers import ExpenseCreationSerializer
from rest_framework.permissions import IsAuthenticated
class ExpenseView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        try:
            serializer = ExpenseCreationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            group_obj = serializer.validated_data.get('group_id')
            amount = serializer.validated_data.get('amount')
            currency = serializer.validated_data.get('currency')
            base_currency = group_obj.base_currency
            if currency==base_currency:
                exchange_rate=1
            else:
                response = requests.get(f'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@2024-03-06/v1/currencies/{currency.lower()}.json')
                data = response.json()
                exchange_rate = data[currency.lower()][base_currency.lower()]
            converted_amount=Decimal(str(amount))*Decimal(str(exchange_rate))
            converted_amount=converted_amount.quantize(Decimal('0.00'))
            splits = serializer.validated_data.get('splits')
            with transaction.atomic():
                expense_obj = Expense.objects.create(converted_amount=converted_amount, currency_used=currency, group=group_obj, amount=amount, payer=request.user)
                expense_obj.save()
                splits_to_create = [ExpenseSplit(user=split['user_id'], amount=Decimal(str(split['amount']))*Decimal(str(exchange_rate)), expense=expense_obj) for split in splits] 
                ExpenseSplit.objects.bulk_create(splits_to_create)
            return Response({"message": "Expense Saved Successfully! "}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            
class GroupBalance(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, group_id):
        try:
            group = Group.objects.prefetch_related('users').get(id=group_id)
            users = group.users.all()            
            annotated_users = users.annotate(
                total_paid = Coalesce(Sum('expense__converted_amount',filter=Q(expense__group=group)), Decimal('0.00')),
                total_owed = Coalesce(Sum('expensesplit__amount',filter=Q(expensesplit__expense__group=group)), Decimal('0.00'))
            )
            balances_list = []

            for user in annotated_users:
                user.balance = user.total_paid - user.total_owed
                balances_list.append({
                    "user_id": user.id,
                    "balance": user.balance
                })        
            return Response({"group_name": group.name, "base_currency":group.base_currency, "balances": balances_list}, status=status.HTTP_201_CREATED)
        except Group.DoesNotExist:
            return Response({"error":"Group does not exist! "},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      