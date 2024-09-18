import re
from collections import defaultdict
from datetime import datetime

log_file_path = r'C:\Users\Brandon\Documents\ERRORES ACCESS LOG\access.log'

anio = input("Introduce el año (formato YYYY): ")
mes = input("Introduce el mes (formato MM): ")

if len(mes) == 1:
    mes = '0' + mes

anio_mes_filtro = f'{anio}-{mes}'

error_counts = defaultdict(int, {'401': 0, '402': 0, '403': 0, '404': 0})

log_pattern = re.compile(r'\[(\d{2}/[A-Za-z]{3}/\d{4}):\d{2}:\d{2}:\d{2}.*?\] "\S+ \S+ \S+" (\d{3})')

def obtener_anio_mes(fecha_str):
    fecha = datetime.strptime(fecha_str, '%d/%b/%Y')
    return fecha.strftime('%Y-%m')

with open(log_file_path, 'r') as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            fecha_log, codigo_estado = match.groups()
            anio_mes = obtener_anio_mes(fecha_log)
            
            if anio_mes == anio_mes_filtro:
                if codigo_estado in error_counts:
                    error_counts[codigo_estado] += 1

print(f"Conteo de errores HTTP para {anio_mes_filtro}:")
for codigo in ['401', '402', '403', '404']:
    print(f"Error {codigo}: {error_counts[codigo]} veces")

