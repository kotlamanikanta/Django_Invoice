from django.urls import path
from .views import *

app_name = "invoice"

urlpatterns = [
    path('invoices/', InvoiceView.as_view(), name='invoice-create'),
    path('invoices/<int:pk>/', InvoiceView.as_view(), name='invoice-update'),


]