from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ErrorDetail

from ..models import Vendor
from ..serializers import VendorSerializer


class TestVendorCreateAPI(APITestCase):
    """
    Test suite to create new vendor instance.
    """

    def setUp(self):

        self.user = User.objects.create_user(username='admin', password='admin123')
        self.vendor_2 = Vendor.objects.create(name="Vendor2", vendor_code="v2")

        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_vendor_create_api(self):
        data = {
            "name": "Vendor1",
            "contact_details": "sample-contact 1",
            "address": "sample-address 1",
            "vendor_code": "v1",
            "on_time_delivery_rate": 1.0,
            "average_response_time": 1.0,
            "fulfillment_rate": 0.0
        }
        response1 = self.client.post('/api/vendors/', data=data)
        vendors = Vendor.objects.all()
        vendor_serializer = VendorSerializer(vendors, many=True)

        self.assertEquals(response1.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response1.data, {'response': 'Vendor created successfully'})

    def test_vendor_create_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        data = {
            "name": "Vendor1",
            "contact_details": "sample-contact 1",
            "address": "sample-address 1",
            "vendor_code": "v1",
            "on_time_delivery_rate": 1.0,
            "average_response_time": 1.0,
            "fulfillment_rate": 0.0
        }
        response = self.client.post(f'/api/vendors/', data=data)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_create_api_if_vendor_code_already_exists(self):
        data = {
            "name": "Vendor2",
            "contact_details": "sample-contact",
            "address": "sample-address",
            "vendor_code": "v2",
            "on_time_delivery_rate": 1.0,
            "average_response_time": 1.0,
            "fulfillment_rate": 0.0
        }
        response = self.client.post(f'/api/vendors/', data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'vendor_code': [ErrorDetail(string='vendor with this vendor code already exists.', code='unique')]})

    def tearDown(self):
        pass


