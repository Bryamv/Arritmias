import numpy as np
import matplotlib.pyplot as plt

# Datos de las dos gráficas
data1 = np.array([-0.30135746, -0.29862286])  # Aquí coloca tus datos para la primera gráfica
data2 = np.array([-0.30852276, -0.3080693])   # Aquí coloca tus datos para la segunda gráfica

# Concatenar los datos
concatenated_data = np.concatenate((data1, data2))

# Crear un arreglo para el eje x
x = np.arange(len(concatenated_data))

# Crear la figura y los ejes
fig, ax = plt.subplots()

# Graficar la serie de datos concatenados
ax.plot(x, concatenated_data)

# Añadir etiquetas y título
ax.set_xlabel('Tiempo')
ax.set_ylabel('Amplitud')
ax.set_title('Electrocardiograma')

# Guardar la gráfica en un archivo
plt.savefig('electrocardiograma.png')

# Mostrar la gráfica resultante
plt.show()
