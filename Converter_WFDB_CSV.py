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
