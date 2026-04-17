from django.urls import path
from payments.views import import_payments   # ✅ IMPORTANT

urlpatterns = [
    path('import/', import_payments, name='import_payments'),
]