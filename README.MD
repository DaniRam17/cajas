# cajas

GESTIÓN DE CAJAS TECNOLÓGICAS - SISTEMA CON LISTAS ENLAZADAS (PYTHON + TKINTER)

Autor: Douglas Daniel Ramirez
Lenguaje: Python 3.12
Interfaz: Tkinter

DESCRIPCIÓN GENERAL
-------------------
Este proyecto permite gestionar el inventario de cajas que contienen equipos tecnológicos, como laptops, desktops, impresoras, celulares y televisores. Las cajas se clasifican por tipo de producto y por estado (Nuevo o Usado). Cada caja se registra con un ID único a nivel global.

TIPO DE DATO ABSTRACTO (TDA) UTILIZADO
--------------------------------------
Se implementa una LISTA ENLAZADA como estructura de almacenamiento para cada tipo y estado de producto. El sistema agrupa las cajas en listas enlazadas organizadas mediante un diccionario.

FUNCIONALIDADES PRINCIPALES
---------------------------
 Registrar nuevas cajas con:
   - ID (único)
   - Tipo de producto (predefinido: Desktop, Laptop, Impresora, Celular, Televisor)
   - Estado (Nuevo o Usado)
   - Si tiene código de barra/QR

Buscar cajas por ID.

Eliminar cajas y liberar el ID para futuros registros.

Ver todo el inventario clasificado por tipo y estado.

Generar reporte filtrado por estado.

Exportar el inventario a un archivo CSV.

Validación para evitar IDs duplicados a nivel global.

REQUISITOS PARA EJECUTAR
------------------------
- Python 3.12 instalado
- Biblioteca estándar (Tkinter viene incluido con Python)
- Archivo principal: cajas.py

¿CÓMO EJECUTAR?
---------------
1. Asegúrate de tener Python instalado.
2. Ejecuta el archivo 'cajas.py':
   > python cajas.py
3. Se abrirá una ventana gráfica para gestionar el inventario.

EXPORTAR A EXE (Opcional)
-------------------------
Si deseas crear un ejecutable (.exe) en Windows:
1. Instala pyinstaller:
   > pip install pyinstaller

2. Genera el ejecutable:
   > pyinstaller --onefile --windowed cajas.py

3. El archivo .exe estará dentro de la carpeta 'dist'.

NOTAS ADICIONALES
-----------------
- Los IDs se guardan en un archivo llamado 'ids_usados.txt' para que el sistema recuerde qué cajas ya han sido registradas incluso al cerrar.
- El archivo CSV se puede generar desde el botón correspondiente y abrirse en Excel.

© 2025 - Proyecto académico para práctica de estructuras de datos con aplicación real.
"""