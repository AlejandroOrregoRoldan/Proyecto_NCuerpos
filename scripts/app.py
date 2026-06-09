import streamlit as st
import pandas as pd
import subprocess
import time

# Configuración de la página
st.set_page_config(page_title="Simulador N-Cuerpos", layout="wide")

st.title("Simulación Paralela de N-Cuerpos")
st.markdown("**Autores:** Alejandro Orrego Roldán y Daniel Duque Rivera")

# Crear pestañas
tab1, tab2, tab3 = st.tabs(["Teoría y Arquitectura", "Demo en Vivo", "Análisis de Rendimiento"])

with tab1:
    st.header("Arquitectura y Fundamentos del Proyecto")
    
    st.subheader("1. El Problema de los N-Cuerpos")
    st.markdown("""
    El problema de los N-cuerpos consiste en predecir los movimientos individuales de un grupo de objetos que interactúan entre sí gravitacionalmente. 
    Para calcular la fuerza neta sobre una sola partícula, es necesario calcular la fuerza que ejercen todas las demás partículas sobre ella utilizando la Ley de Gravitación Universal de Newton:
    """)
    
    # Renderizado matemático de la fórmula
    st.latex(r"F_{ij} = G \frac{m_i m_j}{r^2}")
    
    st.markdown("""
    Donde:
    * **$F_{ij}$** es la fuerza de atracción entre la partícula $i$ y la partícula $j$.
    * **$G$** es la constante de gravitación universal.
    * **$m_i$** y **$m_j$** son las masas de las partículas.
    * **$r$** es la distancia entre ellas.
    """)
    
    st.subheader("2. El Cuello de Botella Computacional")
    st.markdown("""
    Dado que cada partícula interactúa con todas las demás, la complejidad temporal del algoritmo es **$O(N^2)$**. 
    En una simulación con 10,000 partículas, el procesador debe realizar aproximadamente 100 millones de cálculos de fuerza por cada paso de tiempo. 
    Ejecutar esto de forma secuencial (en un solo hilo) asfixia rápidamente a la CPU y subutiliza las arquitecturas multinúcleo modernas, lo que hace indispensable el uso de técnicas de paralelización.
    """)

    st.subheader("3. Estrategia de Paralelización y Sistema Operativo (IPC)")
    st.markdown("""
    Para resolver este problema, implementamos una arquitectura paralela a nivel de Sistema Operativo, dividiendo la carga de trabajo entre múltiples procesos pesados:
    
    * **División del Trabajo:** Si tenemos $N$ partículas y $K$ procesos, cada proceso se encarga de calcular las fuerzas de un bloque exclusivo de $N/K$ partículas.
    * **Memoria Compartida (shmget / shmat):** A diferencia de los hilos tradicionales que comparten memoria implícitamente, utilizamos llamadas directas del sistema (`System V IPC`) para reservar un bloque maestro de memoria RAM en el Kernel. Esto permite que todos los procesos independientes puedan leer y escribir simultáneamente las posiciones del universo sin generar copias de datos innecesarias.
    * **Creación de Procesos (fork):** El proceso padre invoca la llamada al sistema `fork()` para crear los procesos trabajadores.
    * **Sincronización (wait):** El proceso padre se suspende utilizando `wait()` hasta que todos los hijos terminan su porción matemática del trabajo, garantizando que no haya condiciones de carrera al medir los tiempos finales.
    """)

    st.subheader("4. Optimización de Memoria (Structure of Arrays)")
    st.markdown("""
    A nivel de ingeniería de software en C++, en lugar de declarar objetos o estructuras complejas para cada planeta (Arreglo de Estructuras o AoS), organizamos la memoria utilizando arreglos paralelos unidimensionales para las posiciones (X, Y), velocidades (VX, VY) y masas (SoA). Esto maximiza la eficiencia de la memoria caché L1/L2 del procesador, permitiendo lecturas contiguas ultrarrápidas a nivel de hardware.
    """)

with tab2:
    st.header("Demo Interactivo")
    st.write("Prueba la velocidad de nuestra arquitectura en tiempo real.")
    
    col1, col2 = st.columns(2)
    with col1:
        n_particles = st.slider("Número de Partículas (N)", min_value=1000, max_value=20000, step=1000, value=5000)
    with col2:
        k_processes = st.selectbox("Número de Procesos (Hilos)", options=[1, 2, 4, 8, 16], index=2)
    
    if st.button("Ejecutar Simulación"):
        with st.spinner('Calculando gravedad interplanetaria en C++...'):
            start_time = time.time()
            
            # Si elige 1 proceso, ejecutamos el secuencial, sino el paralelo
            if k_processes == 1:
                cmd = ["./bin/sequential", str(n_particles)]
            else:
                cmd = ["./bin/parallel_ipc", str(n_particles), str(k_processes)]
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            try:
                tiempo_c = float(result.stdout.strip())
                st.success("Simulación completada con éxito.")
                st.metric(label="Tiempo de Ejecución Físico", value=f"{tiempo_c:.4f} segundos")
            except ValueError:
                st.error("Hubo un error al ejecutar el binario en C++.")

with tab3:
    st.header("Resultados del Experimento IEEE")
    st.write("Datos extraídos de 30 repeticiones rigurosas para aislar el ruido del Sistema Operativo.")
    
    # --- EL BOTÓN MAESTRO ---
    st.markdown("---")
    st.warning("Nota: Ejecutar el experimento completo toma un par de minutos porque realiza 360 simulaciones matemáticas en segundo plano.")
    
    if st.button("Ejecutar Experimento Completo y Actualizar Gráficas"):
        # 1. Ejecutar el motor estadístico
        with st.spinner('Ejecutando 360 simulaciones. Por favor, no cierres esta ventana...'):
            subprocess.run(["python3", "scripts/experiment.py"])
            
        # 2. Ejecutar el generador de gráficas
        with st.spinner('Dibujando gráficas de alto rendimiento...'):
            subprocess.run(["python3", "scripts/plot_results.py"])
            
        st.success("Base de datos y gráficas actualizadas con éxito.")
    st.markdown("---")

    # --- MOSTRAR DATOS E IMAGEN IEEE ---
    try:
        # Mostrar la tabla CSV
        df = pd.read_csv("data/results.csv")
        st.dataframe(df, use_container_width=True)
        
        # Mostrar la imagen .png con las DOS gráficas
        st.subheader("Gráficas de Rendimiento y Aceleración")
        st.image("docs/rendimiento_ncuerpos.png", caption="Análisis de Rendimiento (Generado por Matplotlib para formato IEEE)", use_container_width=True)
        
    except FileNotFoundError:
        st.error("No se encontraron los datos previos o las gráficas. Haz clic en el botón de arriba para generarlos.")