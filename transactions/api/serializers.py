from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            'amount',
            'account',
            'balance_after_transaction',
            'transaction_type',
        ]