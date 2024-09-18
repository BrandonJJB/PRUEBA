from collections import defaultdict
import re
from datetime import datetime
from tkinter import Tk
from tkinter import filedialog

# Abrir ventana de diálogo para seleccionar archivo
def seleccionar_archivo():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona el archivo de log",
        filetypes=[("Archivos de log", "*.log"), ("Todos los archivos", "*.*")]
    )
    return ruta_archivo

# Función para convertir la fecha en formato 'YYYY-MM'
def extraer_anio_mes(fecha_texto):
    fecha = datetime.strptime(fecha_texto, '%d/%b/%Y')
    return fecha.strftime('%Y-%m')

# Ciclo para permitir múltiples consultas
continuar = True
while continuar:
    # Selección del archivo por el usuario
    ruta_log = seleccionar_archivo()

    # Verificar si se seleccionó un archivo
    if not ruta_log:
        print("No se seleccionó ningún archivo.")
    else:
        # Solicitar el año y mes
        anio_ingresado = input("Introduce el año (formato YYYY): ")
        mes_ingresado = input("Introduce el mes (formato MM): ")

        if len(mes_ingresado) == 1:
            mes_ingresado = '0' + mes_ingresado

        anio_mes_buscado = f'{anio_ingresado}-{mes_ingresado}'

        # Inicializar el diccionario para contar los errores
        conteo_errores = defaultdict(int, {'401': 0, '402': 0, '403': 0, '404': 0})

        # Definir el patrón para extraer la fecha y el código de estado HTTP
        patron_log = re.compile(r'\[(\d{2}/[A-Za-z]{3}/\d{4}):\d{2}:\d{2}:\d{2}.*?\] "\S+ \S+ \S+" (\d{3})')

        # Leer el archivo de log y contar los errores
        try:
            with open(ruta_log, 'r') as archivo:
                for linea in archivo:
                    coincidencia = patron_log.search(linea)
                    if coincidencia:
                        fecha_log, codigo_http = coincidencia.groups()
                        anio_mes_log = extraer_anio_mes(fecha_log)

                        if anio_mes_log == anio_mes_buscado:
                            if codigo_http in conteo_errores:
                                conteo_errores[codigo_http] += 1

            # Mostrar los resultados
            print(f"Conteo de errores HTTP para {anio_mes_buscado}:")
            for codigo in ['401', '402', '403', '404']:
                print(f"Error {codigo}: {conteo_errores[codigo]} veces")

        except FileNotFoundError:
            print("Error: No se encontró el archivo en la ruta proporcionada.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    # Preguntar si el usuario quiere realizar otra consulta
    respuesta = input("¿Quieres realizar otra consulta? (s/n): ").lower()
    if respuesta != 's':
        continuar = False
        print("Programa finalizado.")


