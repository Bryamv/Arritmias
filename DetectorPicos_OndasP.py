import numpy as np
import wfdb
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import pywt
from tensorflow.keras.models import load_model
global model
model = load_model('ten_file_model.h5')

def denoise(data):  
    w = pywt.Wavelet('sym4') 
    maxlev = pywt.dwt_max_level(len(data), w.dec_len) 
    threshold = 0.05 

    coeffs = pywt.wavedec(data, 'sym4', level=maxlev) 
    for i in range(1, len(coeffs)):
        coeffs[i] = pywt.threshold(coeffs[i], threshold*max(coeffs[i])) 
        
    datarec = pywt.waverec(coeffs, 'sym4')
    
    return datarec

def predict_model(signal):
    # Realizar la predicción con el modelo
    predicted_class = model.predict(signal.reshape(1, 360, 1))

    if (np.argmax(predicted_class) != 0):
        return True
    return False
    
## este en teoria detecta ondas P
def detectar_ondas_p(ecg_signal, fs):

    # Detección de picos R (complejos QRS)
    qrs_indices = find_peaks(ecg_signal, height=0.2)[0] 

    # Tomamos el fin y el inicio de la onda P
    p_wave_signals = []
    for qrs_index in qrs_indices:
        # Calcular el inicio y el fin del intervalo para la onda P
        p_start = max(0, qrs_index - 180)  # Evitar índices negativos
        p_end = min(len(ecg_signal), qrs_index + 180)  # Evitar desbordamiento

        # Extraer la señal de la onda P
        p_wave_signal = ecg_signal[p_start:p_end]

        # Guardar la señal de la onda P
        p_wave_signals.append((p_wave_signal, qrs_index/fs))  # Guardar también el tiempo de la onda P

    return p_wave_signals

# Cargar la señal de ECG desde un archivo WFDB
record = wfdb.rdrecord('./100', channels=[0])  # 'archivo_wfdb' es el nombre del archivo WFDB
ecg_signal = record.p_signal.flatten()
fs = record.fs  # Frecuencia de muestreo de la señal de ECG

# Ejemplo de uso
denoised_signal = denoise(ecg_signal)
p_wave_signals = detectar_ondas_p(denoised_signal, fs)

plt.figure(figsize=(10, 6))


for p_wave_signal, time in p_wave_signals: 
    # Asegurar que la señal tenga la longitud correcta
    if len(p_wave_signal) != 360:  # Suponiendo que tu modelo espera una entrada de longitud 360
        continue
    
    predicted_class = predict_model(p_wave_signal)
    
    # Decidir el color de la línea según la predicción
    color = 'red' if predicted_class == True else 'blue'
    
    # Graficar la señal con el color correspondiente
    plt.plot(np.arange(len(p_wave_signal))/fs + time, p_wave_signal, color=color)
    cont = cont + 1

    
    
    

plt.title('Señales de las Ondas P')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
plt.savefig("pico.png")
