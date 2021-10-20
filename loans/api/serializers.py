from rest_framework import serializers

from loans.models import LoanRequests


class LoanRequestSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('loans-api-url:loan-request-detail', lookup_field='slug')

    class Meta:
        model = LoanRequests
        fields = [
            "url",
            'id',
            'amount',
            'request_status',
            'duration_figure',
            'duration',
            'repayment_interval',
            'slug',
            'timestamp',
            'updated',
        ]