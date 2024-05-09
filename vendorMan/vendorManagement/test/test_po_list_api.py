from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Vendor, PurchaseOrder
from ..serializers import PurchaseOrderSerializer


class TestPOListAPI(APITestCase):
    """
    Test suite to list purchase orders, filtered by vendor_code if provided.
    """

    def setUp(self):

        self.user = User.objects.create_user(username='admin', password='admin123')

        self.vendor_1 = Vendor.objects.create(name="Vendor1", vendor_code="v1")
        self.vendor_2 = Vendor.objects.create(name="Vendor2", vendor_code="v2")

        self.po_1 = PurchaseOrder.objects.create(po_number="PO1", quantity=2, status="PENDING", vendor=self.vendor_1)
        self.po_2 = PurchaseOrder.objects.create(po_number="PO2", quantity=3, status="COMPLETED", vendor=self.vendor_1)
        self.po_3 = PurchaseOrder.objects.create(po_number="PO3", quantity=2, status="PENDING", vendor=self.vendor_2)
        self.po_4 = PurchaseOrder.objects.create(po_number="PO4", quantity=5, status="COMPLETED", vendor=self.vendor_2)


        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_po_list_all_api(self):

        response = self.client.get('/api/purchase_orders/')
        po_list = PurchaseOrder.objects.all()
        po_serializer = PurchaseOrderSerializer(po_list, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, po_serializer.data)

    def test_po_list_api_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(f'/api/purchase_orders/')

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_po_list_api_filtered_by_vendor_code(self):
        response = self.client.get(f'/api/purchase_orders/?vendor_code=v1')
        filtered_query = Vendor.objects.get(vendor_code="v1")
        po_list = PurchaseOrder.objects.filter(vendor=filtered_query)
        po_serializer = PurchaseOrderSerializer(po_list, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, po_serializer.data)

    def test_po_list_api_filtered_by_vendor_code_if_vendor_does_not_exist(self):
        response = self.client.get(f'/api/purchase_orders/?vendor_code=v1111')

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {'error': 'Vendor does not exist'})

    def tearDown(self):
        pass


