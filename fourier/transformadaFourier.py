import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración básica
archivo_entrada = 'trayectorias_z_filtrado.csv'
archivo_salida_csv = 'trayectorias_fourier_fft.csv'
archivo_grafica = 'analisis_fourier_fft.png'
fs = 30.0  # Frecuencia de muestreo (30 FPS)
dt = 1.0 / fs

# 1. Cargar las velocidades filtradas en el plano Z
df_z = pd.read_csv(archivo_entrada, index_col='frame')
n_samples = len(df_z)

# 2. Vector de Frecuencias (rfftfreq para señales reales)
freqs = np.fft.rfftfreq(n_samples, d=dt)

# 3. Aplicar FFT a cada columna y extraer magnitud espectral |F(w)|
espectro_magnitudes = {}
for col in df_z.columns:
    espectro_magnitudes[col] = np.abs(np.fft.rfft(df_z[col].values))

# 4. Crear DataFrame con índice en Hertz y exportar CSV
df_fft = pd.DataFrame(espectro_magnitudes, index=freqs)
df_fft.index.name = 'frecuencia_hz'
df_fft.to_csv(archivo_salida_csv)
print(f"CSV con Espectro de Magnitud FFT guardado en: '{archivo_salida_csv}'")

# 5. Generación de Gráficas de Análisis Espectral (Ejemplo con RIGHT_WRIST)
coordenadas = ['RIGHT_WRIST_x', 'RIGHT_WRIST_y', 'RIGHT_WRIST_z']
colores = ['r', 'g', 'b']

fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
for i, col in enumerate(coordenadas):
    axs[i].plot(df_fft.index, df_fft[col], color=colores[i], linewidth=1.5)
    axs[i].set_title(f'Espectro de Magnitud (FFT) - {col}')
    axs[i].set_ylabel('Magnitud Espectral')
    axs[i].grid(True, linestyle='--', alpha=0.6)

axs[2].set_xlabel('Frecuencia (Hz)')
plt.tight_layout()
plt.savefig(archivo_grafica, dpi=300)
plt.close()
print(f"Gráfica guardada en: '{archivo_grafica}'")