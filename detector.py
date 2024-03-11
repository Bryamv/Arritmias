import numpy as np
import wfdb
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt
## este en teoria detecta ondas P
def detectar_ondas_p(ecg_signal, fs):
    # Aplicar un filtro para mejorar la detección de picos
    # Esto puede ayudar a identificar mejor los picos correspondientes a las ondas P
    filtered_ecg_signal = apply_filter(ecg_signal, fs)  # Implementa esta función según tus necesidades

    # Detección de picos R (complejos QRS)
    qrs_indices = find_peaks(filtered_ecg_signal, height=0.2)[0]  # Ajusta el umbral según tus necesidades

    # Identificación de las ondas P antes de cada complejo QRS
    p_wave_starts = []
    p_wave_ends = []
    for qrs_index in qrs_indices:
        # Buscar el punto más cercano antes del complejo QRS
        # donde el valor de la señal sea menor que el punto QRS
        # Esto podría requerir ajuste dependiendo de tus datos
        p_wave_start = np.where(filtered_ecg_signal[:qrs_index] < filtered_ecg_signal[qrs_index])[0][-1]
        p_wave_starts.append(p_wave_start)

        # Identificar el punto más alto de la onda P
        # Esto podría requerir ajuste dependiendo de tus datos
        p_wave_end = np.argmax(filtered_ecg_signal[p_wave_start:qrs_index]) + p_wave_start
        p_wave_ends.append(p_wave_end)

    return p_wave_starts, p_wave_ends

def apply_filter(ecg_signal, fs):
    # Frecuencia de corte para el filtro pasaaltos (ajusta según tus necesidades)
    highcut = 0.5  # Frecuencia de corte en Hz

    # Orden del filtro (ajusta según tus necesidades)
    order = 4

    # Normalización de la frecuencia de corte
    high = highcut / (0.5 * fs)

    # Coeficientes del filtro pasaaltos
    b, a = butter(order, high, btype='high')

    # Aplicar el filtro a la señal de ECG
    filtered_ecg_signal = filtfilt(b, a, ecg_signal)

    return filtered_ecg_signal

# Cargar la señal de ECG desde un archivo WFDB
record = wfdb.rdrecord('./100', channels=[0])  # 'archivo_wfdb' es el nombre del archivo WFDB
ecg_signal = record.p_signal.flatten()
fs = record.fs  # Frecuencia de muestreo de la señal de ECG

# Ejemplo de uso
p_wave_starts, p_wave_ends = detectar_ondas_p(ecg_signal, fs)
print("Puntos de inicio de onda P:", p_wave_starts)
print("Puntos de fin de onda P:", p_wave_ends)
