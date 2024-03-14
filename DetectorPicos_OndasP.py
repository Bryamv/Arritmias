import numpy as np
import wfdb
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import pywt
from tensorflow.keras.models import load_model


def denoise(data):  
    w = pywt.Wavelet('sym4') 
    maxlev = pywt.dwt_max_level(len(data), w.dec_len) 
    threshold = 0.05 

    coeffs = pywt.wavedec(data, 'sym4', level=maxlev) 
    for i in range(1, len(coeffs)):
        coeffs[i] = pywt.threshold(coeffs[i], threshold*max(coeffs[i])) 
        
    datarec = pywt.waverec(coeffs, 'sym4')
    
    return datarec

## este en teoria detecta ondas P
def detectar_ondas_p(ecg_signal, fs):
    # Aplicar un filtro para mejorar la detección de picos
    # Esto puede ayudar a identificar mejor los picos correspondientes a las ondas P
    filtered_ecg_signal = apply_filter(ecg_signal, fs)  # Implementa esta función según tus necesidades

    # Detección de picos R (complejos QRS)
    qrs_indices = find_peaks(filtered_ecg_signal, height=0.2)[0]  # Ajusta el umbral según tus necesidades

    # Tomamos el fin y el inicio de la onda P
    p_wave_signals = []
    for qrs_index in qrs_indices:
        # Calcular el inicio y el fin del intervalo para la onda P
        p_start = max(0, qrs_index - 180)  # Evitar índices negativos
        p_end = min(len(filtered_ecg_signal), qrs_index + 180)  # Evitar desbordamiento

        # Extraer la señal de la onda P
        p_wave_signal = filtered_ecg_signal[p_start:p_end]

        # Guardar la señal de la onda P
        p_wave_signals.append(p_wave_signal)

    return p_wave_signals

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
p_wave_signals = detectar_ondas_p(ecg_signal, fs)
new_signal = denoise(p_wave_signals[6])

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.grid(True)
plt.plot(range(len(new_signal)), new_signal, label=f'Onda P')
plt.subplot(2, 1, 2)
plt.plot(range(len(new_signal)), new_signal, label=f'Onda P sin denoising')
    

plt.title('Señales de las Ondas P')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)
plt.show()


# Cargar el modelo
model = load_model('ten_file_model.h5')

# Predecir la clase de la señal de la onda P
predicted_class = model.predict(new_signal.reshape(1,360,1))
print(f'Clase predicha: {predicted_class}')