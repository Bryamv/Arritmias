import csv
import matplotlib.pyplot as plt

# Nombre del archivo CSV
archivo_csv = '100.csv'

# Listas para almacenar los datos
MLII = []
V5 = []

# Leer el archivo CSV y almacenar los datos en las listas correspondientes
with open(archivo_csv, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Saltar la primera fila si contiene encabezados
    for row in csv_reader:
        MLII.append(float(row[0]))
        V5.append(float(row[1]))

# Crear subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Graficar MLII
axs[0].plot(MLII, label='MLII', color='#26DCAB')  # Modificar color a verde (hexadecimal)
axs[0].set_xlabel('Segundos')
axs[0].set_ylabel('Amplitud')
axs[0].set_title('Gráfico de MLII')
axs[0].grid(True)

# Graficar V5
axs[1].plot(V5, label='V5', color='#0BDB12')  # Modificar color a naranja (hexadecimal)
axs[1].set_xlabel('Segundos')
axs[1].set_ylabel('Amplitud')
axs[1].set_title('Gráfico de V5')
axs[1].grid(True)

# Ajustar el espacio entre subplots
plt.tight_layout()

# Mostrar las gráficas
plt.show()
