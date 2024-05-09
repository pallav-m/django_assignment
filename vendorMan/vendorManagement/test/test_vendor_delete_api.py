from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Vendor
from ..serializers import VendorSerializer


class TestVendorFetchAPI(APITestCase):
    """
    Test suite to delete a vendor instance.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')

        self.vendor_1 = Vendor.objects.create(name="Vendor1", vendor_code="v1")
        self.vendor_2 = Vendor.objects.create(name="Vendor2", vendor_code="v2")

        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_vendor_delete_api(self):
        response = self.client.delete('/api/vendors/1/')

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, {'response': 'Vendor deleted successfully.'})


    def test_vendor_delete_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.delete(f'/api/vendors/2/')

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_delete_api_if_vendor_does_not_exist(self):
        response = self.client.delete(f'/api/vendors/5/')

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'response': 'Vendor does not exist.'})

    def tearDown(self):
        pass
