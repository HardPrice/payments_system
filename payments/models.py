from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal


class Organization(models.Model):
    inn = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}(\d{2})?$',
                message='ИНН должен состоять из 10 или 12 цифр'
            )
        ]
    )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Organization {self.inn}"


class Payment(models.Model):
    operation_id = models.UUIDField(unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payer_inn = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\d{10}(\d{2})?$',
                message='ИНН должен состоять из 10 или 12 цифр'
            )
        ]
    )
    document_number = models.CharField(max_length=20)
    document_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.operation_id}"


class BalanceChange(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Balance change for {self.organization.inn}: {self.amount}"
