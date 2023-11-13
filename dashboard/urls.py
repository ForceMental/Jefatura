from django.urls import path, include
from .views import *

urlpatterns = [
    path('service_venta', obtener_datos_ventas, name='serviceVenta'),
    path('service', external_service_request, name='service'),
    # path('procesar_venta/<int:venta_id>/', ProcesarVentaView.as_view(), name='procesar-venta'), # 'venta_id'
]

