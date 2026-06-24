import streamlit as st
import pandas as pd

# Configuración de la pestaña del navegador
st.set_page_config(page_title="Calculadora de Viento PRO", page_icon="🏃‍♂️", layout="centered")

# Base de datos interna con marcas mínimas oficiales de referencia (RFEA aproximadas PC/AL)
MINIMAS_DB = {
    "Hombre": {
        "60m": {"Absoluto": 6.85, "Sub23": 6.95, "Sub20": 7.05, "Sub18": 7.15, "Sub16": 7.35},
        "100m": {"Absoluto": 10.65, "Sub23": 10.90, "Sub20": 11.15, "Sub18": 11.35, "Sub16": 11.60},
        "200m": {"Absoluto": 21.60, "Sub23": 22.10, "Sub20": 22.55, "Sub18": 22.95}
    },
    "Mujer": {
        "60m": {"Absoluto": 7.65, "Sub23": 7.85, "Sub20": 7.95, "Sub18": 8.05, "Sub16": 8.20},
        "100m": {"Absoluto": 11.95, "Sub23": 12.30, "Sub20": 12.60, "Sub18": 12.75, "Sub16": 12.90},
        "200m": {"Absoluto": 24.45, "Sub23": 25.30, "Sub20": 25.80, "Sub18": 26.30}
    }
}

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

# --- CREACIÓN DE LAS PESTAÑAS ---
tab1, tab2 = st.tabs(["📊 Cálculo Individual & Simulador", "⚔️ Duelo Virtual (Cara a Cara)"])

# ==========================================
# PESTAÑA 1: CÁLCULO INDIVIDUAL + SEMÁFORO + MÍNIMAS + PROYECTOR EN RANGO + WHATSAPP
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
            
            # 1. Semáforo de "Marca Legal"
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

            # 2. NUEVA FUNCIÓN: El Cazador de Mínimas Oficiales
            st.subheader("🎖️ Cazador de Mínimas de España (RFEA)")
            
            minimas_conseguidas = []
            minimas_cercanas = []
            
            if genero in MINIMAS_DB and distancia in MINIMAS_DB[genero]:
                for categoria, marca_minima in MINIMAS_DB[genero][distancia].items():
                    if tiempo_neutral <= marca_minima:
                        minimas_conseguidas.append(categoria)
                    else:
                        diferencia = tiempo_neutral - marca_minima
                        # Si está a menos de 0.60 segundos, la mostramos como "cercana" para motivar
                        if diferencia < 0.60:
                            minimas_cercanas.append((categoria, diferencia, marca_minima))
            
            # Mostrar resultados de mínimas de forma muy visual
            if minimas_conseguidas:
                conseguidas_texto = ", ".join([f"**{c}**" for c in minimas_conseguidas])
                st.balloons()
                st.success(f"🎉 ¡TIENES LA MÍNIMA! Tu tiempo limpio te clasifica para el Campeonato de España en: {conseguidas_texto}")
            else:
                st.info("🏃‍♂️ Sigue entrenando duro, aún no alcanzas la mínima para campeonatos nacionales con esta marca.")
            
            if minimas_cercanas:
                st.write("**🎯 Objetivos a tiro (Mínimas más cercanas):**")
                for cat, dif, m_min in sorted(minimas_cercanas, key=lambda x: x[1]):
                    st.write(f"• A tan solo **{dif:.2f}s** de la mínima **{cat}** ({m_min:.2f}s).")

            st.markdown("---")
            
            # 3. NUEVA FUNCIÓN OPTIMIZADA: Proyector de Marcas Avanzado (En Rango)
            st.subheader("🎯 Proyector de Marcas (Tu Ventana de Potencial)")
            st.write("Dependiendo de si eres un atleta más *Explosivo* (mejor salida) o más *Resistente* (mejor final), tu potencial estimado se encuentra en estos rangos:")
            
            proyecciones_rango = {}
            if distancia == "60m":
                # Proyección a 100m
                f_min_100, f_max_100 = (1.50, 1.57) if genero == "Hombre" else (1.51, 1.58)
                # Proyección a 200m
                f_min_200, f_max_200 = (2.95, 3.20) if genero == "Hombre" else (3.00, 3.25)
                
                proyecciones_rango["100m"] = (tiempo_neutral * f_min_100, tiempo_neutral * f_max_100)
                proyecciones_rango["200m"] = (tiempo_neutral * f_min_200, tiempo_neutral * f_max_200)
                
            elif distancia == "100m":
                # Proyección a 60m
                f_min_60, f_max_60 = (1.57, 1.50) if genero == "Hombre" else (1.58, 1.51)
                # Proyección a 200m
                f_min_200, f_max_200 = (1.96, 2.06) if genero == "Hombre" else (1.98, 2.08)
                
                proyecciones_rango["60m"] = (tiempo_neutral / f_min_60, tiempo_neutral / f_max_60)
                proyecciones_rango["200m"] = (tiempo_neutral * f_min_200, tiempo_neutral * f_max_200)
                
            elif distancia == "200m":
                # Proyección a 100m
                f_min_100, f_max_100 = (2.06, 1.96) if genero == "Hombre" else (2.08, 1.98)
                # Proyección a 60m
                f_min_60, f_max_60 = (3.20, 2.95) if genero == "Hombre" else (3.25, 3.00)
                
                proyecciones_rango["100m"] = (tiempo_neutral / f_min_100, tiempo_neutral / f_max_100)
                proyecciones_rango["60m"] = (tiempo_neutral / f_min_60, tiempo_neutral / f_max_60)
                
            # Mostrar las proyecciones en columnas con el formato de rango
            p_cols = st.columns(len(proyecciones_rango))
            for idx, (dist, (t_min, t_max)) in enumerate(proyecciones_rango.items()):
                p_cols[idx].metric(
                    label=f"Rango Estimado en {dist}", 
                    value=f"{t_min:.2f}s - {t_max:.2f}s",
                    help="El tiempo más rápido corresponde a un perfil optimizado para la distancia; el más lento a uno menos adaptado."
                )
                
            st.markdown("---")
            
            # 4. Tabla de Simulación Automática
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
            
            # 5. Cuadro "Copiar para WhatsApp" con Rangos y Mínimas
            st.subheader("📱 Compartir con el Equipo")
            st.write("Haz clic en el botón de copiar (icono de dos cuadraditos) para pegarlo en WhatsApp:")
            
            # Generar bloque de texto dinámico para WhatsApp de proyecciones en rango
            texto_proyecciones_wa = ""
            for dist, (t_min, t_max) in proyecciones_rango.items():
                texto_proyecciones_wa += f"🎯 *Rango {dist}:* {t_min:.2f}s a {t_max:.2f}s\n"
            
            # Generar bloque de texto dinámico de mínimas
            texto_minimas_wa = "❌ Ninguna actualmente"
            if minimas_conseguidas:
                texto_minimas_wa = "✅ " + ", ".join(minimas_conseguidas)
            elif minimas_cercanas:
                mas_cercana = sorted(minimas_cercanas, key=lambda x: x[1])[0]
                texto_minimas_wa = f"🚀 Rozando {mas_cercana[0]} (a {mas_cercana[1]:.2f}s)"

            texto_whatsapp = (
                f"🏃‍♂️ *¡Resultado de la Calculadora de Viento!*\n"
                f"🏁 *Prueba:* {distancia} ({genero})\n"
                f"⏱️ *Tiempo Real:* {tiempo_real:.2f}s (Viento: {viento:+} m/s)\n"
                f"✨ *Tiempo Neutral (0.0):* {tiempo_neutral:.2f}s\n"
                f"🚦 *Estado:* {estado_legal}\n\n"
                f"🎖️ *Mínimas de España RFEA:*\n"
                f"{texto_minimas_wa}\n\n"
                f"🔮 *Ventana de Potencial Estimado:*\n"
                f"{texto_proyecciones_wa}"
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
