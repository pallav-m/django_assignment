from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Vendor
from ..serializers import VendorSerializer


class TestVendorListAPI(APITestCase):
    """
    Test suite to list vendors
    """

    def setUp(self):

        self.user = User.objects.create_user(username='admin', password='admin123')

        self.vendor_1 = Vendor.objects.create(name="Vendor1", vendor_code="v1")
        self.vendor_2 = Vendor.objects.create(name="Vendor2", vendor_code="v2")

        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_vendor_list_api(self):

        response = self.client.get('/api/vendors/')
        vendors = Vendor.objects.all()
        vendor_serializer = VendorSerializer(vendors, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, vendor_serializer.data)

    def test_vendor_list_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(f'/api/vendors/')

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        pass


