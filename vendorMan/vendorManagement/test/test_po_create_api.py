from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ErrorDetail

from ..models import Vendor
from ..serializers import VendorSerializer


class TestPOCreateAPI(APITestCase):
    """
    Test suite to create new purchase order instance.
    """

    def setUp(self):

        self.user = User.objects.create_user(username='admin', password='admin123')
        self.vendor = Vendor.objects.create(name="Vendor1", vendor_code="v1")

        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_po_create_api(self):
        data = {
              "po_number": "32",
              "quantity": 5,
              "status": "PENDING",
              "vendor": 1
        }
        response = self.client.post('/api/purchase_orders/', data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data, {'response': 'Purchase order created.'})

    def test_po_create_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        data = {
                "po_number": "32",
                "quantity": 5,
                "status": "PENDING",
                "vendor": 0
        }
        response = self.client.post('/api/purchase_orders/', data=data)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_po_create_api_with_invalid_vendor(self):
        data = {
            "po_number": "32",
            "quantity": 5,
            "status": "PENDING",
            "vendor": 15  # this vendor id does not exist.
        }
        response = self.client.post('/api/purchase_orders/', data=data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'vendor': [ErrorDetail(string='Invalid pk "15" - object does not exist.', code='does_not_exist')]})

    def tearDown(self):
        pass


