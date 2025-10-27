import requests
import json
from datetime import datetime

# URL base de tu servicio Backendless
BASE_URL = "https://smartaunt-us.backendless.app/api/data/actividades"

# ----------------------------------------------------
# A. Crear una nueva Actividad (POST)
# ----------------------------------------------------


def create_actividad(descripcion, tipo_actividad, titulo, emocion_asociada):
    payload = {
        "descripcion": descripcion,
        "tipo_actividad": tipo_actividad,
        "titulo": titulo,
        "emocion_asociada": emocion_asociada  # Aquí va el objectId de la emoción
    }

    print("\nIntentando crear una nueva actividad...")
    try:
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            print("\nActividad creada con éxito:")
            return data
        else:
            print(
                f"\nError al crear actividad. Código: {response.status_code}")
            print(f"Respuesta del servidor: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nError de conexión. Verifica la URL del servicio Backendless.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")


# ----------------------------------------------------
# B. Obtener todas las Actividades (GET)
# ----------------------------------------------------


def get_all_actividades():
    print("\nIntentando obtener todas las actividades...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            print("\nLista de actividades obtenida con éxito:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
            return data
        else:
            print(
                f"\nError al obtener actividades. Código: {response.status_code}")
            print(f"Respuesta del servidor: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nError de conexión. Verifica la URL del servicio Backendless.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")


# ----------------------------------------------------
# C. Obtener una Actividad por ID (GET /:id)
# ----------------------------------------------------


def get_actividad_by_id(actividad_id):
    url = f"{BASE_URL}/{actividad_id}"
    print(f"\nIntentando obtener actividad con ID: {actividad_id}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"\nActividad (ID: {actividad_id}) encontrada:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
            return data
        elif response.status_code == 404:
            print(f"\nActividad con ID {actividad_id} no encontrada.")
        else:
            print(
                f"\nError al obtener la actividad. Código: {response.status_code}")
            print(f"Respuesta del servidor: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nError de conexión. Verifica la URL del servicio Backendless.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")


# ----------------------------------------------------
# D. Eliminar una Actividad (DELETE)
# ----------------------------------------------------


def delete_actividad(actividad_id):
    """Elimina una actividad por su ID.

    Retorna True si se eliminó correctamente, False si ocurrió un error
    o None si no se encontró el recurso.
    """
    url = f"{BASE_URL}/{actividad_id}"
    print(f"\nIntentando eliminar actividad con ID: {actividad_id}...")
    try:
        response = requests.delete(url)
        # Backendless suele devolver 200 o 204 en eliminaciones exitosas
        if response.status_code in (200, 204):
            print(f"\nActividad (ID: {actividad_id}) eliminada correctamente.")
            return True
        elif response.status_code == 404:
            print(f"\nActividad con ID {actividad_id} no encontrada.")
            return None
        else:
            print(
                f"\nError al eliminar la actividad. Código: {response.status_code}")
            print(f"Respuesta del servidor: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("\nError de conexión. Verifica la URL del servicio Backendless.")
        return False
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
        return False


# ----------------------------------------------------
# E. Actualizar una Actividad completa (PUT)
# ----------------------------------------------------


def put_actividad(actividad_id, descripcion=None, tipo_actividad=None, titulo=None, emocion_asociada=None, **extra_fields):
    """Actualiza una actividad usando PUT.

    Nota: Backendless no soporta PATCH, por eso usamos PUT también para
    actualizaciones parciales. Solo se incluirán en el payload los campos
    que no sean None (es decir, los proporcionados por el llamador).

    Parámetros conocidos: descripcion, tipo_actividad, titulo, emocion_asociada.
    `extra_fields` permite pasar otros campos adicionales si se necesitan.
    """
    url = f"{BASE_URL}/{actividad_id}"

    # Construir payload solo con los campos provistos (no-None)
    payload = {}
    if descripcion is not None:
        payload["descripcion"] = descripcion
    if tipo_actividad is not None:
        payload["tipo_actividad"] = tipo_actividad
    if titulo is not None:
        payload["titulo"] = titulo
    if emocion_asociada is not None:
        payload["emocion_asociada"] = emocion_asociada

    # Incluir cualquier campo extra provisto vía kwargs
    for k, v in extra_fields.items():
        if v is not None:
            payload[k] = v

    if not payload:
        print("\nNo se proporcionaron campos para actualizar (PUT). Nada que enviar.")
        return None

    print(
        f"\nIntentando actualizar (PUT) actividad con ID: {actividad_id} con campos: {list(payload.keys())}...")
    try:
        response = requests.put(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(
                f"\nActividad (ID: {actividad_id}) actualizada con éxito (PUT):")
            return data
        elif response.status_code == 404:
            print(f"\nActividad con ID {actividad_id} no encontrada.")
        else:
            print(
                f"\nError al actualizar la actividad. Código: {response.status_code}")
            print(f"Respuesta del servidor: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nError de conexión. Verifica la URL del servicio Backendless.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")


# ----------------------------------------------------
# F. Actualizar parcialmente una Actividad (PATCH)
# ----------------------------------------------------
"""

    ----- NO FUNCIONA EN BACKENDLESS -----
    * Se utilizará PUT en su lugar.
"""


def patch_actividad(actividad_id, **fields):
    """Actualiza campos específicos de una actividad usando PATCH.

    `fields` puede contener uno o varios de los campos: descripcion, tipo_actividad,
    titulo, emocion_asociada, etc.
    """
    if not fields:
        print("\nNo se proporcionaron campos para actualizar (PATCH).")
        return None

    url = f"{BASE_URL}/{actividad_id}"
    print(
        f"\nIntentando actualizar (PATCH) actividad con ID: {actividad_id}...")
    try:
        response = requests.patch(url, json=fields)
        if response.status_code == 200:
            data = response.json()
            print(
                f"\nActividad (ID: {actividad_id}) actualizada con éxito (PATCH):")
            return data
        elif response.status_code == 404:
            print(f"\nActividad con ID {actividad_id} no encontrada.")
        else:
            print(
                f"\nError al actualizar la actividad. Código: {response.status_code}")
            print(f"Respuesta del servidor: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nError de conexión. Verifica la URL del servicio Backendless.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
    # Helper para mostrar pasos claros en consola (útil para demos/videos)


# ----------------------------------------------------
# Helper para mostrar pasos claros en consola (útil para demos/videos)
# ----------------------------------------------------


def print_step(number, title, note=None):
    """Imprime un encabezado de paso con separación y timestamp.

    number: número del paso (int o str)
    title: título corto del paso
    note: texto opcional descriptivo
    """
    sep = "=" * 80
    sub = "-" * 80
    ts = datetime.now().isoformat(sep=' ', timespec='seconds')
    print(f"\n{sep}")
    print(f"STEP {number}: {title}    ({ts})")
    if note:
        print(note)
    print(f"{sub}")


def print_step_done(number, msg=None):
    sub = "-" * 40
    print(f"\n{sub} STEP {number} COMPLETED {sub}")
    if msg:
        print(msg)


# ----------------------------------------------------
# Ejemplo de uso (flujo CRUD completo)
# ----------------------------------------------------


if __name__ == '__main__':

    # ----------------------------------------------------
    # Paso 1 — Crear (C de CRUD)
    # Enunciado: Aquí creamos una nueva actividad mediante POST.
    # Resultado esperado: el servidor devuelve la entidad creada con su ID (objectId)
    # ----------------------------------------------------
    print_step(1, "Crear actividad de prueba",
               "Se enviará una petición POST para crear la actividad.")
    nueva = create_actividad(
        descripcion="Escuchar un cuento corto y dibujar tu parte favorita.",
        tipo_actividad="Actividad Literaria",
        titulo="Cuento y dibujo",
        emocion_asociada="tranquilo"
    )

    # ----------------------------------------------------
    # Paso 2 — Listar/Leer (R de CRUD)
    # Enunciado: Solicitamos todas las actividades mediante GET para demostrar lectura de colección.
    # Resultado esperado: una lista (o paginación) con actividades.
    # ----------------------------------------------------
    print_step(2, "Obtener todas las actividades",
               "Se enviará una petición GET para listar actividades.")
    all_act = get_all_actividades()
    if all_act is not None:
        try:
            count = len(all_act) if isinstance(
                all_act, list) else 'desconocido'
        except Exception:
            count = 'desconocido'
        print_step_done(
            2, f"Se obtuvieron {count} actividades.")
    else:
        print_step_done(2, "No se pudieron obtener las actividades.")

    # ----------------------------------------------------
    # Paso 3 — Leer por ID (R de CRUD)
    # Enunciado: Recuperamos la actividad creada por su ID para demostrar lectura de recurso.
    # Resultado esperado: los detalles de la actividad creada.
    # ----------------------------------------------------

    # Validar que la creación fue exitosa antes de continuar, se revisa que el objeto "nueva" tenga "objectId"
    if nueva and "objectId" in nueva:
        print_step(3, "Obtener actividad por ID", f"ID: {nueva['objectId']}")
        get_actividad_by_id(nueva["objectId"])
        print_step_done(3)

        # ----------------------------------------------------
        # Paso 4 — Actualizar completo (U de CRUD) usando PUT
        # Enunciado: Hacemos un PUT que reemplaza campos; aquí lo usamos también
        # como mecanismo para actualizaciones parciales cuando Backendless no soporta PATCH.
        # Resultado esperado: servidor devuelve la entidad actualizada.
        # ----------------------------------------------------
        print_step(4, "Actualizar actividad completamente (PUT)",
                   "Se enviará una petición PUT con solo los campos proporcionados.")
        put_actividad(nueva["objectId"],
                      descripcion="Hacer figuras con plastilina de animales.",
                      tipo_actividad="Actividad Artistica",
                      titulo="Animales en plastilina",
                      emocion_asociada="feliz"
                      )
        print_step_done(4)

        # ----------------------------------------------------
        # Paso 5 — Verificar (R de CRUD)
        # Enunciado: Volvemos a leer el recurso para verificar los cambios aplicados.
        # Resultado esperado: la entidad muestra los campos actualizados.
        # ----------------------------------------------------
        print_step(5, "Verificar actividad actualizada",
                   f"ID: {nueva['objectId']}")
        get_actividad_by_id(nueva["objectId"])
        print_step_done(5)

        # ----------------------------------------------------
        # Paso 6 — Actualización parcial (simulado PATCH vía PUT)
        # Enunciado: Enviar solo los campos a cambiar usando PUT (simula PATCH).
        # Resultado esperado: servidor aplica cambios parciales y devuelve entidad actualizada.
        # ----------------------------------------------------
        print_step(6, "Actualizar parcialmente (simulado PATCH)",
                   "Enviaremos otro PUT con solo los campos a cambiar.")
        put_actividad(nueva["objectId"],
                      titulo="Juega con plastilina",
                      emocion_asociada="alegre"
                      )
        print_step_done(6)

        # ----------------------------------------------------
        # Paso 7 — Verificar (R de CRUD)
        # Enunciado: Volvemos a leer el recurso para verificar los cambios aplicados.
        # Resultado esperado: la entidad muestra los campos actualizados.
        # ----------------------------------------------------
        print_step(7, "Verificar actividad actualizada",
                   f"ID: {nueva['objectId']}")
        get_actividad_by_id(nueva["objectId"])
        print_step_done(7)

        # ----------------------------------------------------
        # Paso 8 — Eliminar (D de CRUD)
        # Enunciado: Eliminamos la actividad creada para cerrar el flujo de demo.
        # Resultado esperado: el servidor confirma la eliminación (200/204).
        # ----------------------------------------------------
        print_step(8, "Eliminar actividad de prueba",
                   f"ID: {nueva['objectId']}")
        delete_actividad(nueva["objectId"])
        print_step_done(8)

        # ----------------------------------------------------
        # Paso 9 — Listar final (verificación de estado)
        # Enunciado: Listamos todas las actividades una vez más para verificar
        # que la actividad creada fue eliminada. En entornos compartidos puede
        # haber otras actividades, así que el conteo es informativo.
        # Resultado esperado: idealmente la lista queda vacía si este es el único
        # recurso creado en el entorno de prueba.
        # ----------------------------------------------------
        print_step(9, "Listar todas las actividades (verificación final)",
                   "Se enviará una petición GET para listar todas las actividades tras la eliminación.")
        all_final = get_all_actividades()
        if all_final is None:
            print_step_done(
                9, "No fue posible obtener la lista final (error en la petición).")
        else:
            try:
                final_count = len(all_final) if isinstance(
                    all_final, list) else 'desconocido'
            except Exception:
                final_count = 'desconocido'
            if final_count == 0:
                print_step_done(9, "Lista vacía — eliminación verificada.")
            else:
                print_step_done(
                    9, f"Lista final contiene {final_count} actividades (no vacía).")

    else:
        # Si la creación falló, no intentamos actualizar/verificar/eliminar
        print_step(3, "Actividad no creada",
                   "Se omiten los pasos de actualización/verificación/eliminación.")
        print_step_done(3)
