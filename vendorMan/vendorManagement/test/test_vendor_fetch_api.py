from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Vendor
from ..serializers import VendorSerializer


class TestVendorFetchAPI(APITestCase):
    """
    Test suite to fetch a single vendor instance.
    """

    def setUp(self):

        self.user = User.objects.create_user(username='admin', password='admin123')

        self.vendor_1 = Vendor.objects.create(name="Vendor1", vendor_code="v1")
        self.vendor_2 = Vendor.objects.create(name="Vendor2", vendor_code="v2")

        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_vendor_fetch_api(self):

        response1 = self.client.get('/api/vendors/1/')
        vendor1 = Vendor.objects.get(id=1)
        vendor_serializer = VendorSerializer(vendor1)

        self.assertEquals(response1.status_code, status.HTTP_200_OK)
        self.assertEquals(response1.data, vendor_serializer.data)

        response2 = self.client.get('/api/vendors/2/')
        vendor2 = Vendor.objects.get(id=2)
        vendor_serializer = VendorSerializer(vendor2)

        self.assertEquals(response2.status_code, status.HTTP_200_OK)
        self.assertEquals(response2.data, vendor_serializer.data)

    def test_vendor_fetch_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(f'/api/vendors/')

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_fetch_api_if_vendor_does_not_exist(self):
        response = self.client.get(f'/api/vendors/5/')

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {'response': 'Vendor does not exist.'})

    def tearDown(self):
        pass


