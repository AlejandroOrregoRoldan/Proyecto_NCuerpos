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
    st.header("Arquitectura del Proyecto")
    st.markdown("""
    Este proyecto resuelve el problema de interacciones gravitacionales usando la Ley de Gravitación Universal de Newton. 
    Dado que su complejidad es **O(N²)**, implementamos paralelismo a nivel de Sistema Operativo.
    
    * **Backend:** C++ para control absoluto de memoria y máximo rendimiento.
    * **IPC (Inter-Process Communication):** Usamos `shmget()` y `fork()` para dividir la carga de partículas entre múltiples procesos hijos sin copiar datos innecesariamente.
    """)

with tab2:
    st.header("Demo Interactivo")
    st.write("Prueba la velocidad de la arquitectura propuesta en tiempo real.")
    
    col1, col2 = st.columns(2)
    with col1:
        n_particles = st.slider("Número de Partículas (N)", min_value=1000, max_value=20000, step=1000, value=5000)
    with col2:
        k_processes = st.selectbox("Número de Procesos (Hilos)", options=[1, 2, 4, 8, 16], index=2)
    
    if st.button("Ejecutar Simulación"):
        with st.spinner('Calculando interacciones en C++...'):
            start_time = time.time()
            
            # Si elige 1 proceso, ejecutamos el secuencial, sino el paralelo
            if k_processes == 1:
                cmd = ["./bin/sequential", str(n_particles)]
            else:
                cmd = ["./bin/parallel_ipc", str(n_particles), str(k_processes)]
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            try:
                tiempo_c = float(result.stdout.strip())
                st.success("Simulación completada.")
                st.metric(label="Tiempo de Ejecución Físico", value=f"{tiempo_c:.4f} segundos")
            except ValueError:
                st.error("Hubo un error al ejecutar el binario en C++.")

with tab3:
    st.header("Resultados del Experimento IEEE")
    st.write("Datos extraídos de 30 repeticiones rigurosas para aislar el ruido del planificador del Sistema Operativo.")
    
    try:
        df = pd.read_csv("data/results.csv")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Gráfica de Aceleración (Speedup)")
        chart_data = df.pivot(index='Procesos', columns='Particulas', values='Speedup')
        st.line_chart(chart_data)
        
    except FileNotFoundError:
        st.warning("No se encontró el archivo de resultados. Ejecute primero el script de experimentación.")