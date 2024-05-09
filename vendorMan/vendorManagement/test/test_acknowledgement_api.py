from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Vendor, PurchaseOrder


class TestAcknowledgementAPI(APITestCase):
    """
    Test suite to acknowledge a purchase order.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')

        self.vendor_1 = Vendor.objects.create(name="Vendor1", vendor_code="v1")

        self.po_1 = PurchaseOrder.objects.create(po_number="PO1", quantity=2, status="PENDING", vendor=self.vendor_1)

        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_po_acknowledgement_api(self):

        response1 = self.client.post('/api/purchase_orders/1/acknowledge/')

        self.assertEquals(response1.status_code, status.HTTP_200_OK)
        self.assertEquals(response1.data, {'response': 'Acknowledged successfully'})

    def test_po_acknowledgement_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.post(f'/api/purchase_orders/1/acknowledge/')

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_po_acknowledge_api_if_vendor_does_not_exist(self):

        response = self.client.post(f'/api/purchase_orders/5/acknowledge/')

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'response': 'Purchase order does not exist.'})

    def tearDown(self):
        pass
