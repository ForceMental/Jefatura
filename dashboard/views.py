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
    url = 'http://107.22.174.168:8010/api/obtener_ventas'
    auth_header = request.headers.get('Authorization')

    try:
        headers = {'Authorization': auth_header} if auth_header else {}

        # Realiza la solicitud GET con el encabezado de autorización
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Procesamiento de datos
            conteo_estado_venta = {"A": 0, "P": 0, "C": 0}
            suma_productos = {}
            conteo_ejecutivo_id = {}
            nombres_ejecutivos = {}  # Diccionario para almacenar nombres de ejecutivos por ID
            conteo_ejecutivos_nombres = {}  # Diccionario para asociar conteo de ejecutivos con sus nombres

            for venta in data:
                estado_venta = venta.get("estado_venta")
                productos = venta.get("productos", [])
                ejecutivo_id = venta.get("ejecutivo_id")
                nombre_ejecutivo = venta.get("nombre_ejecutivo")

                # Incrementar el conteo por estado de venta
                if estado_venta in conteo_estado_venta:
                    conteo_estado_venta[estado_venta] += 1

                # Procesar la suma de productos
                for producto in productos:
                    producto_id = producto.get("id")
                    nombre_producto = producto.get("nombre")
                    cantidad_producto = producto.get("cantidad", 0)

                    nombre_producto = html.unescape(nombre_producto)

                    if producto_id in suma_productos:
                        suma_productos[producto_id]["cantidad"] += cantidad_producto
                    else:
                        suma_productos[producto_id] = {"nombre": nombre_producto, "cantidad": cantidad_producto}

                # Conteo por ejecutivo
                if ejecutivo_id:
                    if ejecutivo_id in conteo_ejecutivo_id:
                        conteo_ejecutivo_id[ejecutivo_id] += 1
                    else:
                        conteo_ejecutivo_id[ejecutivo_id] = 1

                    # Almacenar el nombre del ejecutivo por su ID
                    if ejecutivo_id not in nombres_ejecutivos and nombre_ejecutivo:
                        nombres_ejecutivos[ejecutivo_id] = nombre_ejecutivo

            # Asociar conteo de ejecutivos con sus nombres
            for ejecutivo_id, conteo in conteo_ejecutivo_id.items():
                if ejecutivo_id in nombres_ejecutivos:
                    nombre_ejecutivo = nombres_ejecutivos[ejecutivo_id]
                    conteo_ejecutivos_nombres[nombre_ejecutivo] = conteo

            # Construir resultados
            resultados = {
                "conteo_estado_venta": conteo_estado_venta,
                "suma_productos": suma_productos,
                "conteo_ejecutivo_id": conteo_ejecutivo_id,
                "nombres_ejecutivos": nombres_ejecutivos,
                "conteo_ejecutivos_nombres": conteo_ejecutivos_nombres
            }

            return JsonResponse(resultados, safe=False)

        else:
            return JsonResponse({'error': f'La solicitud GET falló con el código de estado {response.status_code}'})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al realizar la solicitud GET: {e}'})

