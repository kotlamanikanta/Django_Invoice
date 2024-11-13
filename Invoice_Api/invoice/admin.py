from django.contrib import admin
from .models import *
# Register your models here.

class InvoiceAdmin(admin.ModelAdmin):
  list_display = ("id", "invoice_number", "customer_name","date")

admin.site.register(Invoice, InvoiceAdmin)


class InvoiceDetailAdmin(admin.ModelAdmin):
  list_display=("id","invoice")
admin.site.register(InvoiceDetail,InvoiceDetailAdmin)