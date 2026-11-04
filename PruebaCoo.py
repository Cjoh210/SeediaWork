import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf')

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

fuente = "videos/Hola.mp4"  
nombre_archivo_grafica = "trayectoria_brazos.png"
nombre_archivo_csv = "trayectorias_brazos.csv"

cap = cv2.VideoCapture(fuente)
if not cap.isOpened():
    raise RuntimeError(f"Error al abrir la fuente: {fuente}")

# Definir los índices específicos de interés (Hombros, Codos y Muñecas)
indices_interes = [
    mp_pose.PoseLandmark.LEFT_SHOULDER.value,
    mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
    mp_pose.PoseLandmark.LEFT_ELBOW.value,
    mp_pose.PoseLandmark.RIGHT_ELBOW.value,
    mp_pose.PoseLandmark.LEFT_WRIST.value,
    mp_pose.PoseLandmark.RIGHT_WRIST.value
]

nombres_interes = [
    "LEFT_SHOULDER", "RIGHT_SHOULDER",
    "LEFT_ELBOW", "RIGHT_ELBOW",
    "LEFT_WRIST", "RIGHT_WRIST"
]

historial_puntos = []

try:
    print("Procesando video... por favor espera.")
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            puntos_todos = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])
            
            # 1. Calcular el centroide: punto medio de los hombros (clavícula)
            idx_izq = mp_pose.PoseLandmark.LEFT_SHOULDER.value
            idx_der = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
            punto_0 = (puntos_todos[idx_izq] + puntos_todos[idx_der]) / 2.0
            
            # 2. Filtrar únicamente los puntos de interés
            puntos_filtrados = puntos_todos[indices_interes]
            
            # 3. Aplicar transformación lineal (traslación al origen centrado en la clavícula)
            puntos_trasladados = puntos_filtrados - punto_0
            
            historial_puntos.append(puntos_trasladados)

        if cv2.waitKey(1) & 0xFF == 27:  
            break
            
    print("Fin del procesamiento del video.")

finally:
    cap.release()
    pose.close()
    cv2.destroyAllWindows()

if len(historial_puntos) > 0:
    # Convertir a array NumPy: Forma -> (N_frames, 6_landmarks, 3_coords)
    datos = np.array(historial_puntos)
    num_frames, num_landmarks, _ = datos.shape

    # Aplanamos a formato tabular (N_frames, 6 * 3 = 18 columnas)
    datos_2d = datos.reshape(num_frames, num_landmarks * 3)

    # Crear encabezados dinámicos con los 6 puntos seleccionados
    columnas = []
    for nombre in nombres_interes:
        columnas.extend([f"{nombre}_x", f"{nombre}_y", f"{nombre}_z"])

    # Generación y exportación del CSV
    df_trayectorias = pd.DataFrame(datos_2d, columns=columnas)
    df_trayectorias.index.name = 'frame'
    df_trayectorias.to_csv(nombre_archivo_csv)
    print(f"CSV guardado exitosamente en: '{os.path.abspath(nombre_archivo_csv)}'")

    # Generación de la gráfica temporal (Ej: Muñeca derecha normalizada)
    idx_grafica = nombres_interes.index("RIGHT_WRIST")
    trayectoria = datos[:, idx_grafica, :]  # (Frames, 3)

    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    ejes = ['X', 'Y', 'Z']
    colores = ['r', 'g', 'b']
    
    for i in range(3):
        axs[i].plot(trayectoria[:, i], label=f'Coordenada {ejes[i]}', color=colores[i])
        axs[i].set_title(f'RIGHT_WRIST (Relativo a Clavícula) - Coordenada {ejes[i]}')
        axs[i].set_ylabel('Posición Relativa')
        axs[i].grid(True, linestyle='--', alpha=0.6)
        axs[i].legend(loc='upper right')
        
    axs[2].set_xlabel('Frame')
    plt.tight_layout()
    plt.savefig(nombre_archivo_grafica, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Gráfica guardada exitosamente como: '{os.path.abspath(nombre_archivo_grafica)}'")

else:
    print("No se detectó ninguna pose en el video.")