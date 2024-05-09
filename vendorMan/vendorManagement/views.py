from datetime import datetime

from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from .models import Vendor, PurchaseOrder, HistPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceMetricSerializer

from .api_docs import *


# Create your views here.

class VendorView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(**vendor_list_api_schema())
    def get(self, request):
        try:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(**vendor_create_api_schema())
    def post(self, request, *args, **kwargs):
        try:
            serializer = VendorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'response': 'Vendor created successfully'},
                                status=status.HTTP_201_CREATED
                                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('Exception occurred: ', e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_vendor(self, vendor_id):
        """
        Get vendor instance by vendor_id if it exists, otherwise return None.
        """

        try:
            return Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return None

    @swagger_auto_schema(**vendor_fetch_api_schema())
    def get(self, request, vendor_id, *args, **kwargs):
        """
        Retrieve vendor with given id
        """

        try:
            vendor_instance = self.get_vendor(vendor_id)
            if not vendor_instance:
                return Response(
                    {'response': 'Vendor does not exist.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = VendorSerializer(vendor_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(**vendor_update_api_schema())
    def put(self, request, vendor_id, *args, **kwargs):
        """
        Update vendor with given id if it exists
        """

        try:
            vendor_instance = self.get_vendor(vendor_id)
            if not vendor_instance:
                return Response(
                    {'response': 'Vendor does not exist.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = VendorSerializer(vendor_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'response': 'Vendor updated successfully.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('Exception occurred: ', e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(**vendor_delete_api_schema())
    def delete(self, request, vendor_id, *args, **kwargs):
        """
        Delete vendor with given id if it exists
        """

        try:
            vendor_instance = self.get_vendor(vendor_id)
            if not vendor_instance:
                return Response(
                    {'response': 'Vendor does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            vendor_instance.delete()
            return Response(
                {'response': 'Vendor deleted successfully.'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PurchaseOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(**purchase_order_create_api_schema())
    def post(self, request, *args, **kwargs):
        try:
            serializer = PurchaseOrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'response': 'Purchase order created.'},
                                status=status.HTTP_201_CREATED
                                )
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST
                                )

        except Exception as e:
            print(e)
            return Response({'response': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(**purchase_order_list_api_schema())
    def get(self, request, *args, **kwargs):
        """
        Get all purchase orders, filtered by vendor_code if it is provided in the request
        """
        try:
            vendor = request.GET.get('vendor_code')
            if vendor:
                filtered_query = Vendor.objects.get(vendor_code=vendor)
                filtered_po = PurchaseOrder.objects.filter(vendor=filtered_query)
                serializer = PurchaseOrderSerializer(filtered_po, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            po = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(po, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PurchaseOrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_purchase_order(self, po_id):
        """
        Get purchase order instance by po_id if it exists
        :param po_id:
        :return:
        """
        try:
            return PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return None

    @swagger_auto_schema(**purchase_order_fetch_api_schema())
    def get(self, request, po_id, *args, **kwargs):
        try:
            po_instance = self.get_purchase_order(po_id)
            if not po_instance:
                return Response(
                    {'response': 'Purchase order does not exist.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = PurchaseOrderSerializer(po_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(**purchase_order_update_api_schema())
    def put(self, request, po_id, *args, **kwargs):
        try:
            po_instance = self.get_purchase_order(po_id)
            if not po_instance:
                return Response(
                    {'response': 'Purchase order does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = PurchaseOrderSerializer(po_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'response': 'PO updated successfully'},
                                status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(**purchase_order_delete_api_schema())
    def delete(self, request, po_id, *args, **kwargs):
        try:
            po_instance = self.get_purchase_order(po_id)
            if not po_instance:
                return Response(
                    {'response': 'Purchase order does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            po_instance.delete()
            return Response(
                {'response': 'PO deleted successfully.'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorPerformanceMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(**vendor_get_performance_metrics_schema())
    def get(self, request, vendor_id, *args, **kwargs):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = VendorPerformanceMetricSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class AcknowledgeOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, po_id, *args, **kwargs):
        try:
            po_instance = PurchaseOrder.objects.get(id=po_id)
            po_instance.acknowledgement_date = datetime.now()
            po_instance.save()

            return Response({'response': 'Acknowledged successfully'},
                            status=status.HTTP_200_OK)

        except PurchaseOrder.DoesNotExist:
            return Response(
                {'response': 'Purchase order does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print('********', e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
