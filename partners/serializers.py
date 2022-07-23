from rest_framework import serializers
from .models import ExchangePartner









#------------------------------------------------------------------------------
class ExchangePartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangePartner
        fields = ('id', 'name')
