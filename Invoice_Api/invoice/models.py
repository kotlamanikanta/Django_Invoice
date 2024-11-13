from django.db import models
from django.utils import timezone

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer_name}"

class InvoiceDetail(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, related_name="details", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate line_total as quantity * price
        self.line_total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.price}"
