from rest_framework import serializers
from .models import ExchangePartner









#------------------------------------------------------------------------------
class ExchangePartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangePartner
        fields = ('id', 'user_shop', 'partner_shop', 'partnerShopName', 'partner_name', 'partnerShopUser', 'partnerShopPhone', 'partnerShopAddress', 'partnerShopProvince', 'partnerShopCity', 'status')
