import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_plots():
    print("📊 Generando gráficas para el artículo IEEE...")
    
    # Leer los resultados
    df = pd.read_csv("data/results.csv")
    
    # Configurar estilo de los gráficos
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Análisis de Rendimiento: Simulación N-Cuerpos (IPC Memoria Compartida)', fontsize=16, fontweight='bold')

    particles = df['Particulas'].unique()
    colors = ['#e74c3c', '#f39c12', '#2980b9']

    # --- Gráfica 1: Tiempo de Ejecución ---
    for p, color in zip(particles, colors):
        data = df[df['Particulas'] == p]
        ax1.plot(data['Procesos'], data['Tiempo_Promedio_Seg'], marker='o', linewidth=2, color=color, label=f'N={p}')
        
    ax1.set_title('Tiempo de Ejecución vs Número de Procesos', fontsize=12)
    ax1.set_xlabel('Número de Procesos Hijos', fontsize=11)
    ax1.set_ylabel('Tiempo Promedio (Segundos)', fontsize=11)
    ax1.set_xticks([1, 2, 4, 8])
    ax1.legend()

    # --- Gráfica 2: Speedup ---
    # Línea de Speedup Ideal (y = x)
    ax2.plot([1, 2, 4, 8], [1, 2, 4, 8], '--', color='gray', label='Speedup Ideal (Lineal)')
    
    for p, color in zip(particles, colors):
        data = df[df['Particulas'] == p]
        ax2.plot(data['Procesos'], data['Speedup'], marker='s', linewidth=2, color=color, label=f'N={p}')

    ax2.set_title('Aceleración (Speedup) vs Número de Procesos', fontsize=12)
    ax2.set_xlabel('Número de Procesos Hijos', fontsize=11)
    ax2.set_ylabel('Speedup (T_seq / T_par)', fontsize=11)
    ax2.set_xticks([1, 2, 4, 8])
    ax2.legend()

    # Guardar la gráfica en alta calidad para el reporte
    plt.tight_layout()
    os.makedirs("docs", exist_ok=True)
    plt.savefig("docs/rendimiento_ncuerpos.png", dpi=300)
    print("✅ Gráfica guardada con éxito en 'docs/rendimiento_ncuerpos.png'")

if __name__ == "__main__":
    # Requiere instalar pandas y matplotlib si no los tienes: pip install pandas matplotlib
    generate_plots()