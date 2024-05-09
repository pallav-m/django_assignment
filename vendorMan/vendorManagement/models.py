from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

from datetime import datetime


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    vendor_code = models.CharField(unique=True, max_length=255)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')
    )
    po_number = models.CharField(unique=True, max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(default=dict)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.po_number


class HistPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.vendor


@receiver(pre_save, sender=PurchaseOrder, dispatch_uid="purchase_order_analytics")
def trigger_analytics(sender, instance, **kwargs):
    try:
        existing_po = sender.objects.get(id=instance.id)
        vendor = Vendor.objects.get(id=instance.vendor.id)
        if existing_po.status != 'COMPLETED' and instance.status == 'COMPLETED':
            dr = delivery_rate(vendor_id=vendor.id)
            qra = quality_rating_average(vendor_id=vendor.id)
            ffr = fulfillment_rate(vendor_id=instance.vendor.id)
            vendor.on_time_delivery_rate = dr
            vendor.fulfillment_rate = ffr
            vendor.save()
            HistPerformance.objects.create(vendor=vendor, on_time_delivery_rate=dr, quality_rating_avg=qra,
                                           fulfillment_rate=ffr)

        if instance.acknowledgment_date:
            if existing_po.acknowledgment_date != instance.acknowledgment_date:
                art = average_response_time(vendor_id=vendor.id)
                vendor.average_response_time = art
                vendor.save()
    except PurchaseOrder.DoesNotExist:
        # request is a post request.
        pass


def delivery_rate(vendor_id: int) -> float:
    """Calculate the on-time delivery rate for purchase orders."""

    current_time = datetime.now()

    vendor_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id, status='COMPLETED')
    vendor_on_time_delivered = vendor_purchase_orders.filter(delivery_date__lte=current_time)

    if vendor_purchase_orders.count() == 0:
        return 0
    delivery_rate_ratio = vendor_on_time_delivered.count() / vendor_purchase_orders.count()

    return delivery_rate_ratio


def quality_rating_average(vendor_id):
    """Calculate the quality rating of a vendor"""

    vendor_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id, status='COMPLETED')
    vendor_rated_orders = vendor_purchase_orders.exclude(quality_rating=None)

    vendor_ratings = vendor_rated_orders.values('quality_rating')
    if vendor_rated_orders.count() == 0:
        return 0
    average_rating = vendor_ratings / vendor_rated_orders.count()

    return average_rating


def average_response_time(vendor_id):
    """Calculate the average response time for a purchase order"""
    vendor_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id)

    time_diffs = []
    for order in vendor_purchase_orders:

        if not order.acknowledgment_date:
            time_diff = (order.acknowledgment_date - order.issue_date).total_seconds()
            time_diffs.append(time_diff)

    if len(time_diffs) == 0:
        return 0

    average_time_diff = sum(time_diffs) / len(time_diffs)

    return average_time_diff


def fulfillment_rate(vendor_id):
    """Calculate the fulfilment rate for successful orders"""
    vendor_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id)
    successful_orders = vendor_purchase_orders.filter(status='COMPLETED')
    if vendor_purchase_orders.count() == 0:
        return 0

    rate = successful_orders.count() / vendor_purchase_orders.count()

    return rate


