import wfdb
import matplotlib.pyplot as plt

# Ruta al archivo WFDB (.hea y .dat)
ruta_archivo = './100'

# Lectura del archivo WFDB
signals, fields = wfdb.rdsamp(ruta_archivo)

# Obtención de la frecuencia de muestreo
frecuencia_muestreo = fields['fs']

# Tiempo de inicio y final del registro
tiempo_inicio = 0
tiempo_final = len(signals) / frecuencia_muestreo

# Creación de un vector de tiempo
tiempo = [tiempo_inicio + i / frecuencia_muestreo for i in range(len(signals))]

# Graficar las señales de ECG
plt.figure(figsize=(10, 6))
plt.plot(tiempo, signals[:, 0], label='ECG1')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señales de ECG')
plt.legend()
plt.grid(True)
plt.show()
