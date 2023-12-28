from rest_framework import serializers
from .models import Customer, Loan , Eligibility

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['id']


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class EligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility
        fields = '__all__'