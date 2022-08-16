from rest_framework import serializers
from .models import PartnerExchangeNotice
from partners.models import ExchangePartner









#------------------------------------------------------------------------------
class ExchangePartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangePartner
        fields = ('id', 'user_shop', 'partner_shop', 'partnerShopName', 'partner_name', 'partnerShopUser', 'partnerShopPhone', 'partnerShopAddress', 'partnerShopProvince', 'partnerShopCity', 'status')




#------------------------------------------------------------------------------
class PartnerExchangeNoticeSerializer(serializers.ModelSerializer):
    exchange_partner = ExchangePartnerSerializer(read_only=True)
    class Meta:
        model = PartnerExchangeNotice
        fields = '__all__'








#End
