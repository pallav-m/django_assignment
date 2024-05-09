from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Vendor
from ..serializers import VendorSerializer


class TestVendorUpdateAPI(APITestCase):
    """
    Test suite to update a vendor instance.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')

        self.vendor_1 = Vendor.objects.create(name="Vendor1", vendor_code="v1")
        self.vendor_2 = Vendor.objects.create(name="Vendor2", vendor_code="v2")

        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_vendor_update_api(self):
        data1 = {
            "id": 1,
            "name": "Vendor1",
            "contact_details": "sample-contact1",
            "address": "sample-address1",
            "vendor_code": "v1",
            "on_time_delivery_rate": 1.0,
            "average_response_time": 1.0,
            "fulfillment_rate": 0.0
        }

        response1 = self.client.put('/api/vendors/1/', data=data1)
        vendor1 = Vendor.objects.get(id=1)
        vendor_serializer = VendorSerializer(vendor1)

        self.assertEquals(response1.status_code, status.HTTP_200_OK)
        self.assertEquals(response1.data, {'response': 'Vendor updated successfully.'})

    def test_vendor_update_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        data1 = {
            "id": 1,
            "name": "Vendor1",
            "contact_details": "sample-contact1",
            "address": "sample-address1",
            "vendor_code": "v1",
            "on_time_delivery_rate": 1.0,
            "average_response_time": 1.0,
            "fulfillment_rate": 0.0
        }
        response = self.client.put(f'/api/vendors/1/', data=data1)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_update_api_if_vendor_does_not_exist(self):
        data1 = {
            "id": 1,
            "name": "Vendor1",
            "contact_details": "sample-contact1",
            "address": "sample-address1",
            "vendor_code": "v1",
            "on_time_delivery_rate": 1.0,
            "average_response_time": 1.0,
            "fulfillment_rate": 0.0
        }
        response = self.client.put(f'/api/vendors/5/', data=data1)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {'response': 'Vendor does not exist.'})

    def tearDown(self):
        pass
