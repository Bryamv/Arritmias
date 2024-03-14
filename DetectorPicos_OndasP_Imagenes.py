import os
import wfdb
import matplotlib.pyplot as plt

# Crear la carpeta para almacenar las imágenes si no existe
folder_name = '100'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Cargar el archivo WFDB
record = wfdb.rdrecord('100')

# Obtener la señal de ECG
ecg_signal = record.p_signal[:, 0]  # Usar solo una derivación si hay varias

# Obtener las anotaciones de los picos
annotations = wfdb.rdann('100', 'atr')

print(annotations)

# Obtener los índices de los picos R (QRS complexes)
qrs_indices = annotations.sample

# Definir una ventana de tiempo alrededor de cada pico para segmentar
window_size = 100  # Por ejemplo, 100 muestras antes y después de cada pico

# Segmentar cada pico R y guardar las imágenes
for i, index in enumerate(qrs_indices):
    start_index = max(0, index - window_size)
    end_index = min(len(ecg_signal), index + window_size)
    segment = ecg_signal[start_index:end_index]
    
    # Graficar y guardar la imagen
    plt.figure(figsize=(4, 3))
    plt.plot(segment)
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.title(f'Segmento {i}')
    plt.grid(True)
    plt.savefig(os.path.join(folder_name, f'segment_{i}.png'))
    plt.close()

print("Las imágenes se han guardado en la carpeta '100'.")
