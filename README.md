# Simulación Paralela de N-Cuerpos

**Autores:** Alejandro Orrego Roldán y Daniel Duque Rivera  
**Asignatura:** Sistemas Operativos  
**Universidad:** Universidad de Antioquia

---

## Descripción del Proyecto

Este proyecto implementa la simulación del **problema de los N-Cuerpos** — predecir el movimiento de partículas que interactúan gravitacionalmente — con un enfoque en la paralelización a nivel de Sistema Operativo.

Se desarrollaron dos versiones del motor de simulación en **C++**:

- **Secuencial** (`sequential.cpp`): Algoritmo de referencia O(N²) en un solo proceso.
- **Paralela con IPC** (`parallel_ipc.cpp`): Versión que utiliza `fork()`, memoria compartida (`System V IPC: shmget/shmat`) y sincronización con `wait()` para distribuir la carga entre múltiples procesos pesados.

La interfaz visual e interactiva está construida con **Streamlit (Python)** y permite ejecutar demos en vivo y visualizar los resultados del experimento estadístico.

---

## Estructura del Proyecto

```
Proyecto_NCuerpos/
├── src/
│   ├── sequential.cpp       # Motor secuencial en C++
│   └── parallel_ipc.cpp     # Motor paralelo con IPC en C++
├── scripts/
│   ├── app.py               # Interfaz Streamlit
│   ├── experiment.py        # Motor estadístico (30 repeticiones)
│   └── plot_results.py      # Generador de gráficas IEEE
├── bin/                     # Binarios compilados (se generan con make)
├── data/                    # Resultados CSV (se generan al ejecutar el experimento)
├── docs/
│   └── rendimiento_ncuerpos.png  # Gráficas de rendimiento generadas
├── Makefile
└── README.md
```

---

## Requisitos del Sistema

### Sistema Operativo
- **Linux** (Ubuntu 20.04 o superior recomendado) o cualquier distribución compatible con **POSIX**.
  > **IMPORTANTE:** El código paralelo usa `fork()`, `shmget()`, `shmat()` y `sys/wait.h`, que son llamadas al sistema exclusivas de **entornos POSIX (Linux/macOS)**. **No es compatible de forma nativa con Windows**.  
  > En Windows se recomienda usar **WSL 2** (Windows Subsystem for Linux).

### Dependencias de Compilación (C++)
| Herramienta | Versión mínima | Descripción |
|---|---|---|
| `g++` | 9.0+ | Compilador de C++ (GNU) |
| `make` | 4.0+ | Automatización de compilación |
| `libm` | — | Biblioteca matemática (incluida con `g++`) |

### Dependencias de Python
| Paquete | Versión mínima | Descripción |
|---|---|---|
| `Python` | 3.8+ | Intérprete de Python |
| `streamlit` | 1.20+ | Framework para la interfaz web |
| `pandas` | 1.3+ | Manipulación de datos CSV |
| `matplotlib` | 3.4+ | Generación de gráficas |

---

## Instalación de Dependencias

### 1. Instalar dependencias del sistema (Linux / WSL)

```bash
# Actualizar el gestor de paquetes
sudo apt update

# Instalar el compilador g++ y make
sudo apt install -y g++ make
```

### 2. Instalar dependencias de Python

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto:

```bash
# Crear un entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate

# Instalar los paquetes necesarios
pip install streamlit pandas matplotlib
```

---

## Compilación

Desde la raíz del proyecto, ejecuta el Makefile para compilar ambos binarios (secuencial y paralelo):

```bash
# Crear la carpeta bin si no existe
mkdir -p bin

# Compilar ambos binarios
make
```

Esto generará los ejecutables:
- `bin/sequential`
- `bin/parallel_ipc`

Para limpiar los binarios compilados:

```bash
make clean
```

---

## Ejecución de la Aplicación

### Opción A — Interfaz Web Interactiva (Streamlit)

Lanza la aplicación completa con su interfaz gráfica:

```bash
streamlit run scripts/app.py
```

Esto abrirá automáticamente el navegador en `http://localhost:8501`, donde encontrarás tres pestañas:

1. **Teoría y Arquitectura**: Explicación del problema y la estrategia de paralelización.
2. **Demo en Vivo**: Selecciona el número de partículas y procesos y ejecuta la simulación en tiempo real.
3. **Análisis de Rendimiento**: Ejecuta el experimento estadístico completo (360 simulaciones) y visualiza las gráficas.

### Opción B — Ejecución Directa de los Binarios

Puedes ejecutar los programas C++ directamente desde la terminal:

**Versión Secuencial:**
```bash
# Uso: ./bin/sequential [N_partículas]
./bin/sequential 5000
```

**Versión Paralela (IPC):**
```bash
# Uso: ./bin/parallel_ipc [N_partículas] [K_procesos]
./bin/parallel_ipc 5000 4
```

Los programas imprimen por `stdout` el tiempo de ejecución en segundos.

### Opción C — Experimento Estadístico Completo

Para reproducir los datos del reporte IEEE (30 repeticiones por configuración):

```bash
# 1. Ejecutar el motor estadístico (genera data/results.csv)
python3 scripts/experiment.py

# 2. Generar las gráficas de rendimiento (genera docs/rendimiento_ncuerpos.png)
python3 scripts/plot_results.py
```

> ⚠️ El experimento completo realiza **360 simulaciones** y puede tardar varios minutos dependiendo del hardware.

---

## Parámetros Configurables

| Parámetro | Descripción | Valores por defecto |
|---|---|---|
| `N` | Número de partículas | 1000 – 20000 |
| `K` | Número de procesos paralelos | 1, 2, 4, 8, 16 |

> Los valores de `N` y `K` del experimento estadístico se configuran directamente en `scripts/experiment.py`.

---

## Resultados Esperados

Al ejecutar el experimento completo, se generará:
- `data/results.csv` — Tabla con tiempos promedio, desviación estándar y *speedup* por configuración.
- `docs/rendimiento_ncuerpos.png` — Gráficas de rendimiento y aceleración en formato IEEE.
