from drf_yasg import openapi
from rest_framework import status
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceMetricSerializer


def vendor_list_api_schema():
    return {
        'tags': ['Vendors'],
        'manual_parameters': None,
        'responses': {
            status.HTTP_200_OK: VendorSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'List vendors',
        'operation_description': '',
    }


def vendor_create_api_schema():
    return {
        'tags': ['Vendors'],
        'manual_parameters': None,
        'request_body': VendorSerializer,
        'responses': {
            status.HTTP_200_OK: 'Vendor created successfully',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Create a new vendor entry.',
        'operation_description': '',
    }


def vendor_fetch_api_schema():
    return {
        'tags': ['Vendors'],
        'manual_parameters': None,
        'responses': {
            status.HTTP_200_OK: VendorSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Fetch a vendor with vendor_id.',
        'operation_description': '',
    }


def vendor_update_api_schema():
    return {
        'tags': ['Vendors'],
        'manual_parameters': None,
        'request_body': VendorSerializer(),
        'responses': {
            status.HTTP_200_OK: VendorSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Update vendor details with given vendor_id.',
        'operation_description': '',
    }


def vendor_delete_api_schema():
    return {
        'tags': ['Vendors'],
        'manual_parameters': None,
        'responses': {
            status.HTTP_200_OK: 'Vendor deleted successfully',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Delete a vendor with given vendor_id.',
        'operation_description': '',
    }


def vendor_get_performance_metrics_schema():
    return {
        'tags': ['Vendors'],
        'manual_parameters': None,
        'responses': {
            status.HTTP_200_OK: VendorPerformanceMetricSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Retrieve performance metrics for a vendor with given vendor id.',
        'operation_description': '',
    }


def purchase_order_create_api_schema():
    return {
        'tags': ['Purchase Order'],
        'manual_parameters': None,
        'request_body': PurchaseOrderSerializer,
        'responses': {
            status.HTTP_200_OK: 'Purchase order created.',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Create Purchase Order',
        'operation_description': '',
    }


def purchase_order_list_api_schema():
    return {
        'tags': ['Purchase Order'],
        'manual_parameters': [
            openapi.Parameter('vendor_code', openapi.IN_QUERY, description="Vendor code", type=openapi.TYPE_STRING,
                              required=False), ],
        'responses': {
            status.HTTP_200_OK: PurchaseOrderSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'List purchase orders.',
        'operation_description': '',
    }


def purchase_order_fetch_api_schema():
    return {
        'tags': ['Purchase Order'],
        'manual_parameters': None,
        'responses': {
            status.HTTP_200_OK: VendorSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Fetch a purchase order with given po_id.',
        'operation_description': '',
    }


def purchase_order_update_api_schema():
    return {
        'tags': ['Purchase Order'],
        'manual_parameters': None,
        'request_body': PurchaseOrderSerializer(),
        'responses': {
            status.HTTP_200_OK: PurchaseOrderSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Update purchase order with given po_id.',
        'operation_description': '',
    }


def purchase_order_delete_api_schema():
    return {
        'tags': ['Purchase Order'],
        'manual_parameters': None,
        'responses': {
            status.HTTP_200_OK: 'Purchase order deleted successfully',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        'operation_summary': 'Delete a purchase order with given po_id.',
        'operation_description': '',
    }
