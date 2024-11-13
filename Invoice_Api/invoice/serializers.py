from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'description', 'quantity', 'price', 'line_total']

    # Validation for quantity: must be greater than 0
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    # Validation for price: must be greater than 0
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    # Object-level validation to automatically calculate line_total
    def validate(self, data):
        data['line_total'] = data['quantity'] * data['price']
        return data


class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True)  # Nested serializer for InvoiceDetails

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'customer_name', 'date', 'details']

    # Validation for invoice_number: must be unique
    def validate_invoice_number(self, value):
        if self.instance is None and Invoice.objects.filter(invoice_number=value).exists():
            raise serializers.ValidationError("Invoice number must be unique.")
        return value

    # Object-level validation for the Invoice and its details
    def validate(self, data):
        # Ensure there is at least one detail
        if not data.get('details'):
            raise serializers.ValidationError("Invoice must contain at least one item in details.")

        return data

    def create(self, validated_data):
        # Create Invoice and related InvoiceDetails
        details_data = validated_data.pop('details')
        invoice = Invoice.objects.create(**validated_data)
        
        for detail_data in details_data:
            # Calculate line_total for each detail based on quantity * price
            detail_data['line_total'] = detail_data['quantity'] * detail_data['price']
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        
        return invoice

    def update(self, instance, validated_data):
        # Update Invoice
        details_data = validated_data.pop('details')
        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        # Update related InvoiceDetails
        existing_detail_ids = [detail.id for detail in instance.details.all()]
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id and detail_id in existing_detail_ids:
                # Update existing InvoiceDetail
                detail_instance = InvoiceDetail.objects.get(id=detail_id, invoice=instance)
                detail_instance.description = detail_data.get('description', detail_instance.description)
                detail_instance.quantity = detail_data.get('quantity', detail_instance.quantity)
                detail_instance.price = detail_data.get('price', detail_instance.price)
                detail_instance.line_total = detail_instance.quantity * detail_instance.price
                detail_instance.save()
            else:
                # Create new InvoiceDetail
                detail_data['line_total'] = detail_data['quantity'] * detail_data['price']
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        return instance
