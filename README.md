# Demo CRUD con Backendless (actividades)

Este repositorio contiene un script de ejemplo `crud.py` que demuestra
las operaciones CRUD (Create, Read, Update, Delete) sobre una tabla
llamada `actividades` en un Backend-as-a-Service (BaaS) — concretamente
Backendless.

El objetivo principal fue: implementar las operaciones HTTP necesarias,
permitir usar `PUT` para simulacros de `PATCH` (porque Backendless no
soporta PATCH en este caso), y mostrar en consola pasos claros y
separados para facilitar una demo en video.

## Qué cambié / añadí

- `crud.py`:
  - Funciones para cada operación:
    - `create_actividad(...)` — POST (crear)
    - `get_all_actividades()` — GET (listar)
    - `get_actividad_by_id(id)` — GET (leer por id)
    - `put_actividad(id, ...)` — PUT (actualizar — implementado para enviar
      sólo los campos proporcionados, permitiendo usar PUT como PATCH)
    - `patch_actividad(id, **fields)` — PATCH (incluida, pero Backendless no
      la soporta; se mantiene por completitud)
    - `delete_actividad(id)` — DELETE (eliminar)
  - Helpers de consola para demos:
    - `print_step(number, title, note=None)` — imprime encabezado con timestamp
    - `print_step_done(number, msg=None)` — imprime fin de paso
  - Bloque `__main__` con flujo paso-a-paso (1..8) que representa todos los
    estados CRUD y muestra en consola lo que se ejecuta (útil para grabar un video):
    1) Crear, 2) Listar, 3) Leer por ID, 4) Actualizar (PUT), 5) Actualizar parcial (PUT como PATCH),
    6) Verificar, 7) Eliminar, 8) Listar final para verificar el estado.

## Entorno y dependencias

- Entorno del contenedor de desarrollo: Debian GNU/Linux 13 (trixie).
- Python: se usa un entorno virtual (por ejemplo `/app/.venv` en el contenedor).
- Dependencias principales:
  - `requests` — para enviar peticiones HTTP.

Instalación mínima (desde la carpeta del proyecto):

```bash
# crear/activar venv (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install requests
```

## BaaS usado

Se está utilizando Backendless como BaaS. La base URL usada en `crud.py` es:

```
https://smartaunt-us.backendless.app/api/data/actividades
```

Esto apunta a una tabla llamada `actividades` en el servicio Backendless.
Ten en cuenta que el script realiza llamadas reales a esa URL, por lo que
las operaciones CREATE y DELETE modificarán datos reales si el endpoint
está activo y tienes permisos.

## Cómo ejecutar

Ejecuta el script desde la raíz del proyecto con el venv activado:

```bash
python crud.py
```

Salida esperada (resumida):
- Verás pasos numerados (STEP 1..8) con timestamps, la respuesta del servidor
  para cada petición y mensajes de finalización por paso.

Advertencia: el script ejecuta operaciones destructivas (DELETE). Úsalo
en un entorno de prueba o modifica el código para no ejecutar el bloque
`__main__` si no deseas afectar datos reales.

## Notas técnicas y decisiones

- Backendless no soporta PATCH en el entorno utilizado, así que `put_actividad`
  fue diseñado para aceptar parámetros opcionales y construir un `payload`
  con sólo los campos no-None. Así es posible usar PUT como PATCH (actualización parcial).
- Se añadió `patch_actividad(...)` por completitud, pero en práctica el flujo
  de demo usa `put_actividad` para actualizaciones parciales.
- Se agregó un helper visual (separadores y timestamps) para que la demo en
  video muestre claramente qué paso se está ejecutando.

## Sugerencias y mejoras futuras

- Añadir una opción `--dry-run` o una variable de entorno `DRY_RUN=1` para
  simular las peticiones sin enviarlas al BaaS (útil para demos sin tocar datos).
- Añadir confirmación interactiva antes de ejecutar operaciones destructivas
  (por ejemplo, antes de DELETE).
- Añadir tests (pytest) que mockeen las llamadas a `requests` para validar
  la lógica sin tocar el servicio remoto.
- Registrar las respuestas a un fichero de log (niveles INFO/DEBUG) para
  poder revisar la demo más tarde.

## Conclusiones de la actividad

- Se implementó un cliente CRUD sencillo y didáctico que cubre los casos
  habituales de crear, leer, actualizar y eliminar recursos.
- Debido a limitaciones del BaaS (ausencia de PATCH), la solución adapta
  PUT para realizar actualizaciones parciales, lo cual es una técnica
  práctica cuando el servidor lo permite.
- La salida de consola fue mejorada para ser clara en una demostración,
  mostrando paso, timestamp y resultado esperado, lo que facilita la
  comunicación en un video o presentación.

Si quieres, puedo:
- Añadir un `README` más detallado con ejemplos de salida copiable.
- Implementar `--dry-run` en `crud.py` y documentarlo aquí.
- Añadir tests unitarios que mockeen `requests`.
