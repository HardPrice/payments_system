from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from decimal import Decimal
import logging

from .models import Payment, Organization, BalanceChange
from .serializers import PaymentWebhookSerializer, OrganizationBalanceSerializer

logger = logging.getLogger(__name__)


class BankWebhookView(APIView):
    def post(self, request):
        serializer = PaymentWebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Проверяем, существует ли уже такой платеж
        if Payment.objects.filter(operation_id=data['operation_id']).exists():
            return Response({'status': 'Payment already processed'}, status=status.HTTP_200_OK)

        try:
            with transaction.atomic():
                # Создаем или получаем организацию
                organization, _ = Organization.objects.get_or_create(
                    inn=data['payer_inn']
                )

                # Создаем платеж
                payment = Payment.objects.create(
                    operation_id=data['operation_id'],
                    amount=data['amount'],
                    payer_inn=data['payer_inn'],
                    document_number=data['document_number'],
                    document_date=data['document_date']
                )

                # Обновляем баланс организации
                old_balance = organization.balance
                organization.balance += data['amount']
                organization.save()

                # Логируем изменение баланса
                BalanceChange.objects.create(
                    organization=organization,
                    payment=payment,
                    amount=data['amount'],
                    balance_after=organization.balance
                )

                logger.info(
                    f"Balance updated for organization {data['payer_inn']}: "
                    f"old={old_balance}, new={organization.balance}, "
                    f"operation_id={data['operation_id']}"
                )

                return Response({'status': 'success'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrganizationBalanceView(APIView):
    def get(self, request, inn):
        organization = get_object_or_404(Organization, inn=inn)
        serializer = OrganizationBalanceSerializer(organization)
        return Response(serializer.data)



