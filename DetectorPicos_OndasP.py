import numpy as np
import wfdb
from scipy.signal import find_peaks
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
    qrs_indices = find_peaks(ecg_signal, height= 0.2)[0] 

    # Tomamos el fin y el inicio de la onda P
    vector_p_wave = []
    for qrs_index in qrs_indices:
        # Calcular el inicio y el fin del intervalo para la onda P
        p_start = max(0, qrs_index - 180)  # Evitar índices negativos
        p_end = min(len(ecg_signal)-1, qrs_index + 180)  # Evitar desbordamiento

        # Extraer la señal de la onda P
        vector_p_wave.append([p_start, p_end])

    return np.array(vector_p_wave)

# Cargar la señal de ECG desde un archivo WFDB
record = wfdb.rdrecord('./100', channels=[0])  # 'archivo_wfdb' es el nombre del archivo WFDB
ecg_signal = record.p_signal.flatten()
fs = record.fs  # Frecuencia de muestreo de la señal de ECG

# Ejemplo de uso
denoised_signal = denoise(ecg_signal)#x_signal
p_wave_signals = detectar_ondas_p(denoised_signal, fs)#x_waves points
p_wave_signals = np.unique(p_wave_signals.flatten())
print(p_wave_signals.shape)
# print(p_wave_signals)
X_mask = np.zeros(len(denoised_signal))
print(p_wave_signals)
X_mask[p_wave_signals] = 1
print(X_mask)
# print(len(X_mask))
# print(p_wave_signals)
plt.plot(denoised_signal, label='Ondas P', color='r')
# plt.plot(X_mask*denoised_signal, label='Ondas P', color='r')
plt.plot(np.abs(X_mask-1)*denoised_signal, label='ECG', color='b')
plt.show()