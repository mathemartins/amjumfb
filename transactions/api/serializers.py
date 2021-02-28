from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            'company',
            'amount',
            'account',
            'balance_after_transaction',
            'transaction_type',
            'timestamp',
        ]