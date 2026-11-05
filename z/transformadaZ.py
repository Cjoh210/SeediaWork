import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Configuración básica
archivo_entrada = 'trayectorias_brazos.csv'
archivo_salida_csv = 'trayectorias_z_filtrado.csv'
archivo_grafica = 'analisis_transformada_z.png'
fs = 30.0  # Frecuencia de muestreo (30 FPS)
dt = 1.0 / fs

# 1. Cargar el CSV procesado previamente
df = pd.read_csv(archivo_entrada, index_col='frame')

# 2. Calcular los vectores de velocidad (derivada temporal)
df_velocidades = df.diff().fillna(0.0) / dt

# 3. Diseño del Filtro Digital IIR en Plano Z (Butterworth pasa-bajos)
nyquist = fs / 2.0
cutoff = 8.0  # Frecuencia de corte para eliminar ruido acelerado de MediaPipe
b, a = signal.butter(2, cutoff / nyquist, btype='low')

# 4. Aplicar el filtro digital de fase cero (filtfilt) a todas las columnas
df_z_filtrado = pd.DataFrame(
    signal.filtfilt(b, a, df_velocidades.values, axis=0),
    columns=df_velocidades.columns,
    index=df.index
)

# 5. Exportar el CSV filtrado en Z
df_z_filtrado.to_csv(archivo_salida_csv)
print(f"CSV procesado en plano Z guardado en: '{archivo_salida_csv}'")

# 6. Generación de Gráficas de Análisis (Ejemplo con RIGHT_WRIST)
coordenadas = ['RIGHT_WRIST_x', 'RIGHT_WRIST_y', 'RIGHT_WRIST_z']
colores = ['r', 'g', 'b']

fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
for i, col in enumerate(coordenadas):
    axs[i].plot(df_velocidades[col], label='Velocidad Cruda', color='orange', alpha=0.5, linestyle='--')
    axs[i].plot(df_z_filtrado[col], label='Velocidad Filtrada (Plano Z)', color=colores[i], linewidth=1.8)
    axs[i].set_title(f'Filtrado Digital (Plano Z) - {col}')
    axs[i].set_ylabel('Velocidad (unidades/s)')
    axs[i].grid(True, linestyle='--', alpha=0.6)
    axs[i].legend(loc='upper right')

axs[2].set_xlabel('Frame')
plt.tight_layout()
plt.savefig(archivo_grafica, dpi=300)
plt.close()
print(f"Gráfica guardada en: '{archivo_grafica}'")