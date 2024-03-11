import wfdb
import pandas as pd

def wfdb_to_csv(record_name, output_csv):
    # Cargar los datos del archivo WFDB
    signals, fields = wfdb.rdsamp(record_name)

    # Obtener los nombres de las columnas
    column_names = fields['sig_name']

    # Crear un DataFrame de Pandas con los datos
    df = pd.DataFrame(signals, columns=column_names)

    # Guardar el DataFrame como un archivo CSV
    df.to_csv(output_csv, index=False)

# Nombre del archivo WFDB sin la extensión
record_name = './100'

# Nombre del archivo CSV de salida
output_csv = '100.csv'

# Llamar a la función para convertir el archivo WFDB a CSV
wfdb_to_csv(record_name, output_csv)


import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV convertido desde el archivo WFDB
df = pd.read_csv(output_csv)

# Graficar todas las señales
plt.figure(figsize=(12, 6))

# Suponiendo que df es tu DataFrame y 'columna' es el nombre de la columna que deseas sacar
columna_extraida = df['V5']


plt.plot(columna_extraida.index, columna_extraida, label='V5')

# Ajustar la leyenda y etiquetas de los ejes
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.title('Señales del archivo WFDB convertido a CSV')
plt.grid(True)

# Mostrar la gráfica
plt.show()
