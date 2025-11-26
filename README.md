1.  **Modelos (`test_models.py`)**:
    *   Probé que se puedan crear juegos en la base de datos correctamente.
    *   Usé una base de datos en memoria (SQLite) para no usar la base de datos real.

2.  **Rutas (`test_routes.py`)**:
    *   `test_index`: Chequé que la página de inicio cargue bien (código 200).
    *   `test_profile_requires_login`: Verifiqué la seguridad. Intenté entrar a `/agregar_juego` sin loguearme y confirmé que me manda al login (código 302).

3.  **API (`test_api.py`)**:
    *   `test_get_juegos`: Probé que el endpoint `/api/juegos` responda bien y devuelva la lista de juegos en formato JSON.

## Retos que me encontré y cómo los resolví

1.  **El nombre de la carpeta**:
    *   Al principio Python no encontraba los tests porque la carpeta se llamaba `test` y yo ponía `tests` en el comando. Lo arreglé ejecutando el comando con el nombre correcto: `python -m unittest discover -v test`.

2.  **Faltaban librerías**:
    *   Me salían errores porque faltaban instalar algunas librerias.

3.  **Problemas con los imports**:
    *   Tuve un problema importando los modelos en los tests porque `app` no es un paquete. Lo solucioné cambiando los imports para traer `Juego` directo desde `models.py`.