from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Vendor
from ..serializers import VendorPerformanceMetricSerializer


class VendorPerformanceMetricsTestCase(APITestCase):
    """
    Test suite for vendor performance metrics API
    """

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')

        self.vendor_1 = Vendor.objects.create(name="Vendor1", vendor_code="v1", on_time_delivery_rate=1.0,
                                              average_response_time=2.5, fulfillment_rate=1.5)

        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_vendor_performance_metrics(self):
        response = self.client.get('/api/vendors/1/performance/')
        vendor = Vendor.objects.get(id=1)
        serializer = VendorPerformanceMetricSerializer(vendor)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_vendor_performance_metrics_without_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get('/api/vendors/1/performance/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
