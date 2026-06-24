import streamlit as st
import pandas as pd

# Configuración de la pestaña del navegador
st.set_page_config(page_title="Calculadora de Viento PRO", page_icon="🏃‍♂️", layout="centered")

# Función interna para obtener el coeficiente según tus reglas
def obtener_coeficiente(distancia, genero):
    if distancia == "60m":
        return 0.030 if genero == "Hombre" else 0.025
    elif distancia == "100m":
        return 0.055 if genero == "Hombre" else 0.050
    elif distancia == "200m":
        return 0.090 if genero == "Hombre" else 0.080
    return 0.0

# Títulos principales de la web
st.title("🏃‍♂️ Calculadora de Viento Neutral PRO 🏃‍♀️")
st.write("La herramienta definitiva para el análisis de marcas de velocidad sin influencia del viento.")

# --- CREACIÓN DE LAS PESTAÑAS (Ahora solo 2) ---
tab1, tab2 = st.tabs(["📊 Cálculo Individual & Simulador", "⚔️ Duelo Virtual (Cara a Cara)"])

# ==========================================
# PESTAÑA 1: CÁLCULO INDIVIDUAL + SIMULACIÓN + SEMÁFORO + WHATSAPP
# ==========================================
with tab1:
    st.header("⚡ Analizar una Marca")
    
    # Inputs organizados en columnas
    col1, col2 = st.columns(2)
    with col1:
        distancia = st.selectbox("Selecciona la distancia:", ["60m", "100m", "200m"], index=None, placeholder="Elige una prueba...")
        tiempo_real = st.number_input("Tiempo registrado (segundos):", value=None, min_value=0.0, step=0.01, placeholder="Ej: 11.28", key="ind_time")
    with col2:
        viento = st.number_input("Viento medido (m/s):", value=None, step=0.1, placeholder="Ej: +2.3 o -1.5", key="ind_wind")
        genero = st.radio("Género del atleta:", ["Hombre", "Mujer"], index=None, horizontal=True, key="ind_gen")

    # Botón de ejecución
    if st.button("🚀 Calcular Rendimiento Completo", type="primary", key="btn_individual"):
        if distancia is None or tiempo_real is None or viento is None or genero is None:
            st.error("⚠️ Por favor, rellena todos los campos antes de calcular.")
        else:
            coef = obtener_coeficiente(distancia, genero)
            tiempo_neutral = tiempo_real + (viento * coef)
            
            st.markdown("---")
            
            # Idea: Semáforo de "Marca Legal"
            st.subheader("🚦 Homologación de la Marca")
            if viento > 2.0:
                st.warning(f"🟠 **Marca No Homologable:** El viento a favor ({viento:+} m/s) supera el límite legal reglamentario de +2.0 m/s.")
                estado_legal = "No Legal (+2.0)"
            else:
                st.success(f"🟢 **Marca 100% Legal:** El viento de {viento:+} m/s cumple con la normativa para récords y mínimas.")
                estado_legal = "Legal"
            
            # Resultado Principal
            st.markdown(f"### ⏱️ Tu tiempo con viento neutral (0.0) sería: **{tiempo_neutral:.2f}s**")
            
            st.markdown("---")
            
            # Idea: Tabla de Simulación Automática
            st.subheader("📊 Tabla de Simulación de Vientos")
            st.write("Esto es lo que habrías registrado hoy si las condiciones climáticas hubieran sido diferentes:")
            
            vientos_simular = [-2.0, -1.0, 0.0, 1.0, 2.0]
            filas_simulacion = []
            for v in vientos_simular:
                t_estimado = tiempo_neutral - (v * coef)
                nota = "Neutral" if v == 0.0 else ("Límite Legal" if v == 2.0 else "")
                filas_simulacion.append({
                    "Viento Simulado": f"{v:+} m/s" if v != 0 else "0.0 m/s",
                    "Tiempo Estimado": f"{t_estimado:.2f}s",
                    "Nota": nota
                })
            
            df_sim = pd.DataFrame(filas_simulacion)
            st.dataframe(df_sim, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Idea: Cuadro "Copiar para WhatsApp"
            st.subheader("📱 Compartir con el Equipo")
            st.write("Haz clic en el botón de copiar (icono de dos cuadraditos arriba a la derecha del recuadro gris) para pegarlo en WhatsApp:")
            
            texto_whatsapp = (
                f"🏃‍♂️ *¡Resultado de la Calculadora de Viento!*\n"
                f"🏁 *Prueba:* {distancia} ({genero})\n"
                f"⏱️ *Tiempo Real:* {tiempo_real:.2f}s (Viento: {viento:+} m/s)\n"
                f"✨ *Tiempo Neutral (0.0):* {tiempo_neutral:.2f}s\n"
                f"🚦 *Estado:* {estado_legal}"
            )
            st.code(texto_whatsapp, language="text")


# ==========================================
# PESTAÑA 2: COMPARADOR CARA A CARA (DUELO VIRTUAL)
# ==========================================
with tab2:
    st.header("⚔️ Duelo Virtual de Atletas")
    st.write("¿Quién ha sido realmente más rápido? Compara a dos atletas que corrieron en series diferentes con vientos distintos.")
    
    duelo_distancia = st.selectbox("Selecciona la distancia del duelo:", ["60m", "100m", "200m"], index=1)
    
    col_at1, col_at2 = st.columns(2)
    
    with col_at1:
        st.markdown("### 🏃‍♂️ Atleta 1")
        nom1 = st.text_input("Nombre Atleta 1:", value="Atleta A")
        t1 = st.number_input("Tiempo registrado (s):", value=None, min_value=0.0, step=0.01, placeholder="Ej: 10.95", key="t1")
        v1 = st.number_input("Viento medido (m/s):", value=None, step=0.1, placeholder="Ej: +1.5", key="v1")
        g1 = st.radio("Género Atleta 1:", ["Hombre", "Mujer"], index=0, key="g1", horizontal=True)
        
    with col_at2:
        st.markdown("### 🏃‍♀️ Atleta 2")
        nom2 = st.text_input("Nombre Atleta 2:", value="Atleta B")
        t2 = st.number_input("Tiempo registrado (s):", value=None, min_value=0.0, step=0.01, placeholder="Ej: 11.12", key="t2")
        v2 = st.number_input("Viento medido (m/s):", value=None, step=0.1, placeholder="Ej: -0.8", key="v2")
        g2 = st.radio("Género Atleta 2:", ["Hombre", "Mujer"], index=0, key="g2", horizontal=True)

    if st.button("🔥 ¡Iniciar Duelo Virtual!", type="primary"):
        if t1 is None or v1 is None or t2 is None or v2 is None:
            st.error("⚠️ Es obligatorio rellenar los tiempos y vientos de ambos atletas para simular el duelo.")
        else:
            coef1 = obtener_coeficiente(duelo_distancia, g1)
            coef2 = obtener_coeficiente(duelo_distancia, g2)
            
            n1 = t1 + (v1 * coef1)
            n2 = t2 + (v2 * coef2)
            
            st.markdown("### 🏆 Veredicto del Duelo Virtual")
            st.write(f"👉 Ajustado a viento cero, el tiempo de **{nom1}** equivale a: **{n1:.2f}s**")
            st.write(f"👉 Ajustado a viento cero, el tiempo de **{nom2}** equivale a: **{n2:.2f}s**")
            
            if abs(n1 - n2) < 0.001:
                st.info(f"🤝 **¡Empate técnico absoluto!** En condiciones neutrales perfectas, ambos habrían clavado la misma marca.")
            elif n1 < n2:
                diferencia = n2 - n1
                st.success(f"👑 **¡Ganador Virtual: {nom1}!** Corriendo sin la influencia del viento, habría aventajado a {nom2} por **{diferencia:.2f}s**.")
            else:
                diferencia = n1 - n2
                st.success(f"👑 **¡Ganador Virtual: {nom2}!** Corriendo sin la influencia del viento, habría aventajado a {nom1} por **{diferencia:.2f}s**.")
