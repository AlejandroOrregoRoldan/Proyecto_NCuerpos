import subprocess
import statistics
import csv
import os

# --- CONFIGURACIÓN DEL EXPERIMENTO ---
PARTICLES = [1000, 5000, 10000]
PROCESSES = [2, 4, 8]  # El caso de 1 proceso se cubre con el código secuencial
REPETITIONS = 30
RESULTS_FILE = "data/results.csv"

def run_program(cmd):
    """Ejecuta un comando en la terminal y captura el tiempo de salida."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        # El programa en C++ solo imprime el tiempo, lo convertimos a float
        return float(result.stdout.strip())
    except ValueError:
        print(f"[ERROR] Salida inesperada del comando {' '.join(cmd)}: {result.stdout}")
        return None

def main():
    print("Iniciando Experimento de N-Cuerpos (30 Repeticiones por caso)...\n")
    
    # Preparamos el archivo CSV para guardar los resultados
    with open(RESULTS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Encabezados del CSV (Perfecto para tu reporte IEEE)
        writer.writerow(["Particulas", "Procesos", "Tiempo_Promedio_Seg", "Desviacion_Estandar", "Speedup"])
        
        for N in PARTICLES:
            print(f"--- Evaluando Universo con {N} partículas ---")
            
            # 1. Medir el Baseline (Secuencial = 1 Hilo)
            print("  Ejecutando Secuencial (1 proceso)...", end="", flush=True)
            seq_times = []
            for _ in range(REPETITIONS):
                t = run_program(["./bin/sequential", str(N)])
                if t is not None:
                    seq_times.append(t)
            
            seq_mean = statistics.mean(seq_times)
            seq_stdev = statistics.stdev(seq_times)
            print(f" {seq_mean:.4f}s (±{seq_stdev:.4f})")
            
            # Guardar el Baseline en el CSV
            writer.writerow([N, 1, round(seq_mean, 4), round(seq_stdev, 4), 1.00])
            
            # 2. Medir el Código Paralelo (2, 4 y 8 procesos)
            for K in PROCESSES:
                print(f"  Ejecutando Paralelo ({K} procesos)...", end="", flush=True)
                par_times = []
                for _ in range(REPETITIONS):
                    t = run_program(["./bin/parallel_ipc", str(N), str(K)])
                    if t is not None:
                        par_times.append(t)
                
                par_mean = statistics.mean(par_times)
                par_stdev = statistics.stdev(par_times)
                speedup = seq_mean / par_mean
                print(f" {par_mean:.4f}s (±{par_stdev:.4f}) -> Speedup: {speedup:.2f}x")
                
                # Guardar en el CSV
                writer.writerow([N, K, round(par_mean, 4), round(par_stdev, 4), round(speedup, 2)])
            print() # Salto de línea visual
            
    print(f"✅ Experimento completado. Resultados guardados en '{RESULTS_FILE}'.")

if __name__ == "__main__":
    # Asegurarnos de que las carpetas existan
    os.makedirs("data", exist_ok=True)
    main()