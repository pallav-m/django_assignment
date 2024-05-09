from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class VendorPerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'on_time_delivery_rate', 'average_response_time', 'fulfillment_rate']