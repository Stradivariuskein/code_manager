# import sys
# from django.apps import AppConfig
# from django.db import connections
# from django.db.utils import OperationalError
# from django.core.management import call_command

# class CoreConfig(AppConfig):
#     name = 'apps.core'

#     def ready(self):
#         if 'runserver' not in sys.argv:
#             return  # evitar que se ejecute en shell, test, etc.

#         default_db = connections['default']
#         try:
#             # Intentar abrir una conexión para verificar si la DB existe
#             default_db.ensure_connection()
#         except OperationalError:
#             print("📂 Base de datos no encontrada. Creando migraciones y aplicando migrate...")
#             try:
#                 call_command('makemigrations', interactive=False)
#                 call_command('migrate', interactive=False)
#                 print("✅ Migraciones completadas.")
#             except Exception as e:
#                 print(f"❌ Error al crear/aplicar migraciones: {e}")
#         else:
#             print("🗂️ Base de datos ya existente. No se ejecutan migraciones iniciales.")
