from rest_framework import serializers
from .models import Payment, Organization


class PaymentWebhookSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    payer_inn = serializers.CharField(max_length=12)
    document_number = serializers.CharField(max_length=20)
    document_date = serializers.DateTimeField()


class OrganizationBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['inn', 'balance']



