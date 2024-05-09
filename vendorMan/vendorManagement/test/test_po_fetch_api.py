from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Vendor, PurchaseOrder
from ..serializers import VendorSerializer, PurchaseOrderSerializer


class TestVendorFetchAPI(APITestCase):
    """
    Test suite to fetch a single purchase order.
    """

    def setUp(self):

        self.user = User.objects.create_user(username='admin', password='admin123')

        self.vendor_1 = Vendor.objects.create(name="Vendor1", vendor_code="v1")

        self.po_1 = PurchaseOrder.objects.create(po_number="PO1", quantity=2, status="PENDING", vendor=self.vendor_1)
        self.po_2 = PurchaseOrder.objects.create(po_number="PO2", quantity=3, status="COMPLETED", vendor=self.vendor_1)


        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_po_fetch_api(self):

        response1 = self.client.get('/api/purchase_orders/1/')
        po1 = PurchaseOrder.objects.get(id=1)
        po_serializer = PurchaseOrderSerializer(po1)

        self.assertEquals(response1.status_code, status.HTTP_200_OK)
        self.assertEquals(response1.data, po_serializer.data)

        response2 = self.client.get('/api/purchase_orders/2/')
        po2 = PurchaseOrder.objects.get(id=2)
        po_serializer = PurchaseOrderSerializer(po2)

        self.assertEquals(response2.status_code, status.HTTP_200_OK)
        self.assertEquals(response2.data, po_serializer.data)

    def test_po_fetch_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(f'/api/purchase_orders/')

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_po_fetch_api_if_po_does_not_exist(self):
        response = self.client.get(f'/api/purchase_orders/5/')

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {'response': 'Purchase order does not exist.'})

    def tearDown(self):
        pass


