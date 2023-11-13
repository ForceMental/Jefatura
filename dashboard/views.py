from django.shortcuts import render
import requests
from django.http import JsonResponse
import html

def external_service_request(request):
    
    url = 'http://107.22.174.168:8000/api/visitas/'

    
    response = requests.get(url)

    
    if response.status_code == 200:
        
        data = response.json()
        print(data)
        
        contador_reprogramadas = {"True": 0, "False": 0}
        contadores_empleado = {}
        contador_finalizada = {"True": 0, "False": 0}
        contador_tipo_visita = {"A": 0, "F": 0}

        
        for visita in data:
            empleado_id = visita["empleado_id"]
            reprogramada = visita["reprogramada"]
            finalizada = visita["finalizada"]
            tipo_visita = visita["tipo_visita"]

            
            contador_reprogramadas[str(reprogramada)] += 1

            
            if empleado_id in contadores_empleado:
                contadores_empleado[empleado_id] += 1
            else:
                contadores_empleado[empleado_id] = 1

            
            contador_finalizada[str(finalizada)] += 1

            
            contador_tipo_visita[tipo_visita] += 1

        contadores = {
            "contador_reprogramadas": contador_reprogramadas,
            "contadores_empleado": contadores_empleado,
            "contador_finalizada": contador_finalizada,
            "contador_tipo_visita": contador_tipo_visita
        }

        
        print(contador_reprogramadas)
        print(contadores_empleado)
        print(contador_finalizada)
        print(contador_tipo_visita)
        return JsonResponse(contadores, safe=False)
    else:
        return JsonResponse({'error': 'La solicitud al servicio externo falló.'}, status=response.status_code)

def obtener_datos_ventas(request):
    url = 'http://107.22.174.168:8030/api/ventas/'  # URL de la solicitud GET

    try:
        
        response = requests.get(url)

        
        if response.status_code == 200:
            
            data = response.json()

            
            conteo_estado_venta = {"A": 0, "P": 0, "C": 0}
            suma_productos = {}
            conteo_ejecutivo_id = {}

            
            for venta in data:
                estado_venta = venta.get("estado_venta")
                productos = venta.get("productos", [])
                ejecutivo_id = venta.get("ejecutivo_id")

               
                if estado_venta in conteo_estado_venta:
                    conteo_estado_venta[estado_venta] += 1

                
                for producto in productos:
                    producto_id = producto.get("id")
                    nombre_producto = producto.get("nombre")
                    cantidad_producto = producto.get("cantidad", 0)

                    
                    nombre_producto = html.unescape(nombre_producto)

                    if producto_id in suma_productos:
                        suma_productos[producto_id]["cantidad"] += cantidad_producto
                    else:
                        suma_productos[producto_id] = {"nombre": nombre_producto, "cantidad": cantidad_producto}

                
                if ejecutivo_id:
                    if ejecutivo_id in conteo_ejecutivo_id:
                        conteo_ejecutivo_id[ejecutivo_id] += 1
                    else:
                        conteo_ejecutivo_id[ejecutivo_id] = 1

            
            resultados = {
                "conteo_estado_venta": conteo_estado_venta,
                "suma_productos": suma_productos,
                "conteo_ejecutivo_id": conteo_ejecutivo_id
            }

            return JsonResponse(resultados, safe=False)

        else:
            return JsonResponse({'error': f'La solicitud GET falló con el código de estado {response.status_code}'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al realizar la solicitud GET: {e}'})
