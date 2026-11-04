import matplotlib.pyplot as plt

archivo = 'data.csv'  # Asegúrate de que está en la misma carpeta

x1, y1 = [], []
x2, y2 = [], []
x3, y3 = [], []

# --- Leer y parsear ---
with open(archivo, 'r', encoding='utf-8') as f:
    for linea in f:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split('|')
        for idx, parte in enumerate(partes):
            # Eliminar paréntesis y dividir por coma y espacio
            coords = parte.strip('()').split(', ')
            x = int(coords[0])
            y = int(coords[1])
            if idx == 0:
                x1.append(x); y1.append(y)
            elif idx == 1:
                x2.append(x); y2.append(y)
            elif idx == 2:
                x3.append(x); y3.append(y)

# El tiempo es el índice de la lista (fotograma)
frames = list(range(len(x1)))

# ------------------------------------------------------------
# GRÁFICO 1: X vs Tiempo (arriba) y Y vs Tiempo (abajo)
# ------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# X vs tiempo
ax1.plot(frames, x1, label='Columna 1 - X', marker='o', markersize=4, linestyle='-', linewidth=1)
ax1.plot(frames, x2, label='Columna 2 - X', marker='s', markersize=4, linestyle='-', linewidth=1)
ax1.plot(frames, x3, label='Columna 3 - X', marker='^', markersize=4, linestyle='-', linewidth=1)
ax1.set_ylabel('Coordenada X', fontsize=12)
ax1.set_title('Evolución de la coordenada X en el tiempo (fotogramas)', fontsize=13)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Y vs tiempo
ax2.plot(frames, y1, label='Columna 1 - Y', marker='o', markersize=4, linestyle='-', linewidth=1)
ax2.plot(frames, y2, label='Columna 2 - Y', marker='s', markersize=4, linestyle='-', linewidth=1)
ax2.plot(frames, y3, label='Columna 3 - Y', marker='^', markersize=4, linestyle='-', linewidth=1)
ax2.set_xlabel('Número de fotograma (tiempo)', fontsize=12)
ax2.set_ylabel('Coordenada Y', fontsize=12)
ax2.set_title('Evolución de la coordenada Y en el tiempo (fotogramas)', fontsize=13)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('tiempo_vs_coordenadas_XY.png', dpi=150)
print("✅ Gráfico 1 guardado como 'tiempo_vs_coordenadas_XY.png'")

# ------------------------------------------------------------
# GRÁFICO 2: Un subplot por punto (X e Y juntas)
# ------------------------------------------------------------
fig2, axes = plt.subplots(1, 3, figsize=(15, 5))

datos_puntos = [
    (x1, y1, 'Punto 1 (Columna 1)'),
    (x2, y2, 'Punto 2 (Columna 2)'),
    (x3, y3, 'Punto 3 (Columna 3)')
]

for i, (xs, ys, titulo) in enumerate(datos_puntos):
    ax = axes[i]
    ax.plot(frames, xs, label='Coordenada X', color='red', marker='o', markersize=4, linewidth=1)
    ax.plot(frames, ys, label='Coordenada Y', color='blue', marker='s', markersize=4, linewidth=1)
    ax.set_title(titulo, fontsize=12)
    ax.set_xlabel('Fotograma', fontsize=10)
    ax.legend()
    ax.grid(True, alpha=0.3)

fig2.suptitle('Evolución de X e Y por cada punto a lo largo del tiempo', fontsize=14)
plt.tight_layout()
plt.savefig('tiempo_vs_XY_por_punto.png', dpi=150)
print("✅ Gráfico 2 guardado como 'tiempo_vs_XY_por_punto.png'")

plt.close('all')
print("¡Proceso completado! Revisa los archivos PNG generados.")