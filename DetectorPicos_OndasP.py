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

    # Detección de picos R (complejos QRS)
    qrs_indices = find_peaks(ecg_signal, height= 0.2)[0] 

    # Tomamos el fin y el inicio de la onda P
    p_wave_signals = []
    for qrs_index in qrs_indices:
        # Calcular el inicio y el fin del intervalo para la onda P
        p_start = max(0, qrs_index - 180)  # Evitar índices negativos
        p_end = min(len(ecg_signal), qrs_index + 180)  # Evitar desbordamiento

        # Extraer la señal de la onda P
        p_wave_signal = ecg_signal[p_start:p_end]

        # Guardar la señal de la onda P
        p_wave_signals.append(p_wave_signal)

    return p_wave_signals

# Cargar la señal de ECG desde un archivo WFDB
record = wfdb.rdrecord('./100', channels=[0])  # 'archivo_wfdb' es el nombre del archivo WFDB
ecg_signal = record.p_signal.flatten()
fs = record.fs  # Frecuencia de muestreo de la señal de ECG

# Ejemplo de uso
denoised_signal = denoise(ecg_signal)
p_wave_signals = detectar_ondas_p(denoised_signal, fs)

#graficar el pico de onda R
plt.figure(figsize=(10, 6))
plt.grid(True)
print(len(p_wave_signals[1]))
plt.plot(range(len(p_wave_signals[1])), p_wave_signals[1], label=f'Onda P', color='red')



    

plt.title('Señales de las Ondas P')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)
plt.show()


# Cargar el modelo
model = load_model('ten_file_model.h5')

# Predecir la clase de la señal de la onda P
# predicted_class = model.predict(new_signal.reshape(1,360,1))
# print(f'Clase predicha: {predicted_class}')