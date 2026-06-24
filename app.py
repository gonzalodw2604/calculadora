import streamlit as st
import pandas as pd

# Configuración de la pestaña del navegador
st.set_page_config(page_title="Calculadora de Viento PRO", page_icon="🏃‍♂️", layout="centered")

# Base de datos interna con marcas mínimas oficiales de referencia (RFEA aproximadas PC/AL)
# ¡Actualizada con categorías Máster de 35 a 55 años!
MINIMAS_DB = {
    "Hombre": {
       "100m": {"Absoluto": 10.60, "Sub23": 10.75, "Sub20": 10.85, "Sub18": 11.05, "Sub16": 11.45, "M35": 11.31, "M40": 11.70, "M45": 11.85, "M50": 12.04, "M55": 12.42, "M60": 12.93},
        "200m": {"Absoluto": 21.40, "Sub23": 21.75, "Sub20": 22.00, "Sub18": 22.40, "M35": 23.02, "M40": 23.60, "M45": 24.07, "M50": 24.69, "M55": 25.78, "M60": 27.04},
        "400m": {"Absoluto": 47.80, "Sub23": 48.00, "Sub20": 48.75, "Sub18": 49.75, "M35": 51.15, "M40": 53.17, "M45": 53.14, "M50": 56.14, "M55": 57.97, "M60": 61.82}
    },
    "Mujer": {
       "100m": {"Absoluto": 11.90, "Sub23": 12.05, "Sub20": 12.30, "Sub18": 12.25, "Sub16": 12.55, "F35": 13.08, "F40": 13.49, "F45": 13.76, "F50": 13.98, "F55": 14.67, "F60": 15.10},
        "200m": {"Absoluto": 24.30, "Sub23": 24.85, "Sub20": 25.20, "Sub18": 25.25, "F35": 26.42, "F40": 27.95, "F45": 28.56, "F50": 28.60, "F55": 30.19, "F60": 32.06},
        "400m": {"Absoluto": 54.50, "Sub23": 56.25, "Sub20": 57.10, "Sub18": 57.75, "F35": 61.15, "F40": 62.69, "F45": 64.29, "F50": 65.95, "F55": 68.18, "F60": 74.29}
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
    elif distancia == "400m":
        return 0.0  # El viento no afecta de forma neta/oficial en los 400m
    return 0.0

# Títulos principales de la web
st.title("🏃‍♂️ Calculadora de Viento Neutral para TheBalasTeam 🏃‍♀️")
st.write("La herramienta definitiva para el análisis de marcas de velocidad sin influencia del viento.")

# --- CREACIÓN DE LAS PESTAÑAS ---
tab1, tab2 = st.tabs(["📊 Cálculo Individual & Simulador", "⚔️ Duelo Virtual (Cara a Cara)"])

# ==========================================
# PESTAÑA 1: CÁLCULO INDIVIDUAL + SEMÁFORO + MÍNIMA PERSONALIZADA + PROYECTOR EN RANGO + WHATSAPP
# ==========================================
with tab1:
    st.header("⚡ Analizar una Marca")
    
    # Inputs organizados en columnas
    col1, col2 = st.columns(2)
    with col1:
        distancia = st.selectbox("Selecciona la distancia:", ["60m", "100m", "200m", "400m"], index=None, placeholder="Elige una prueba...")
        tiempo_real = st.number_input("Tiempo registrado (segundos):", value=None, min_value=0.0, step=0.01, placeholder="Ej: 11.28", key="ind_time")
    with col2:
        # Si elige 400m, el viento es irrelevante reglamentariamente (Usamos key distinta para evitar bug de caché)
        if distancia == "400m":
            viento = st.number_input("Viento medido (m/s):", value=0.0, step=0.1, disabled=True, help="En los 400m no se mide el viento reglamentariamente.", key="ind_wind_400")
        else:
            viento = st.number_input("Viento medido (m/s):", value=None, step=0.1, placeholder="Ej: +2.3 o -1.5", key="ind_wind")
            
        genero = st.radio("Género del atleta:", ["Hombre", "Mujer"], index=None, horizontal=True, key="ind_gen")

    # SELECTOR: Elección de categoría/campeonato objetivo (Con opciones Máster añadidas)
    lista_categorias = ["Absoluto", "Sub23", "Sub20", "Sub18", "Sub16", "Máster 35", "Máster 40", "Máster 45", "Máster 50", "Máster 55"]
    categoria_elegida = st.selectbox("🏆 Selecciona tu categoría (Campeonato de España):", lista_categorias, index=None, placeholder="Elige tu campeonato destino...")

    # Botón de ejecución
    if st.button("🚀 Calcular Rendimiento Completo", type="primary", key="btn_individual"):
        if distancia is None or tiempo_real is None or viento is None or genero is None or categoria_elegida is None:
            st.error("⚠️ Por favor, rellena todos los campos (incluyendo tu categoría) antes de calcular.")
        else:
            coef = obtener_coeficiente(distancia, genero)
            tiempo_neutral = tiempo_real + (viento * coef)
            
            st.markdown("---")
            
            # 1. Semáforo de "Marca Legal"
            st.subheader("🚦 Homologación de la Marca")
            if distancia == "400m":
                st.success("🟢 **Marca Oficial:** En los 400m no aplica el límite de viento al dar una vuelta completa a la pista. ¡Tu marca es totalmente válida!")
                estado_legal = "Válida (No aplica viento)"
            elif viento > 2.0:
                st.warning(f"🟠 **Marca No Homologable:** El viento a favor ({viento:+} m/s) supera el límite legal reglamentario de +2.0 m/s.")
                estado_legal = "No Legal (+2.0)"
            else:
                st.success(f"🟢 **Marca 100% Legal:** El viento de {viento:+} m/s cumple con la normativa para récords y mínimas.")
                estado_legal = "Legal"
            
            # Resultado Principal
            if distancia == "400m":
                st.markdown(f"### ⏱️ Tu tiempo neto es: **{tiempo_neutral:.2f}s**")
            else:
                st.markdown(f"### ⏱️ Tu tiempo con viento neutral (0.0) sería: **{tiempo_neutral:.2f}s**")
            
            st.markdown("---")

            # 2. El Cazador de Mínimas enfocado en TU Campeonato elegido
            st.subheader(f"🎖️ Objetivo: Campeonato de España {categoria_elegida}")
            
            texto_minimas_wa = ""
            if categoria_elegida in MINIMAS_DB[genero].get(distancia, {}):
                marca_minima = MINIMAS_DB[genero][distancia][categoria_elegida]
                
                if tiempo_neutral <= marca_minima:
                    diferencia = marca_minima - tiempo_neutral
                    st.balloons()
                    if diferencia == 0:
                        st.success(f"🔥 ¡MÍNIMA CLAVADA! Has hecho exactamente los **{marca_minima:.2f}s** exigidos. ¡Estás dentro del Campeonato de España!")
                        texto_minimas_wa = f"✅ ¡MÍNIMA CLAVADA para el España {categoria_elegida}! ({marca_minima:.2f}s)"
                    else:
                        st.success(f"🎉 ¡TIENES LA MÍNIMA! Tu tiempo limpio ({tiempo_neutral:.2f}s) rebaja la mínima ({marca_minima:.2f}s) por **{diferencia:.2f}s**. ¡A preparar las maletas!")
                        texto_minimas_wa = f"✅ ¡Mínima conseguida para el España {categoria_elegida}! (Te han sobrado {diferencia:.2f}s)"
                else:
                    diferencia = tiempo_neutral - marca_minima
                    st.warning(f"🎯 Te has quedado a tan solo **{diferencia:.2f}s** de la mínima exigida ({marca_minima:.2f}s). ¡Está cerquísima, en la próxima carrera cae seguro!")
                    texto_minimas_wa = f"🚀 Rozando la mínima {categoria_elegida} (a sólo {diferencia:.2f}s de los {marca_minima:.2f}s)"
            else:
                if distancia == "400m" and categoria_elegida == "Sub16":
                    st.info(f"ℹ️ Curiosidad: La RFEA no contempla los 400m en Sub16. En esta categoría la prueba oficial de la vuelta a la pista es el **300m lisos**.")
                else:
                    st.info(f"ℹ️ Curiosidad: La RFEA no contempla la distancia de {distancia} para el Campeonato de España {categoria_elegida}.")
                texto_minimas_wa = f"ℹ️ Sin prueba oficial de {distancia} en {categoria_elegida}"

            st.markdown("---")
            
            # 3. Proyector de Marcas Avanzado (En Rango)
            st.subheader("🎯 Proyector de Marcas (Tu Ventana de Potencial)")
            st.write("Dependiendo de si eres un atleta más *Explosivo* o más *Resistente*, tu potencial estimado se encuentra en estos rangos:")
            
            proyecciones_rango = {}
            if distancia == "60m":
                f_min_100, f_max_100 = (1.50, 1.57) if genero == "Hombre" else (1.51, 1.58)
                f_min_200, f_max_200 = (2.95, 3.20) if genero == "Hombre" else (3.00, 3.25)
                proyecciones_rango["100m"] = (tiempo_neutral * f_min_100, tiempo_neutral * f_max_100)
                proyecciones_rango["200m"] = (tiempo_neutral * f_min_200, tiempo_neutral * f_max_200)
                
            elif distancia == "100m":
                f_min_60, f_max_60 = (1.57, 1.50) if genero == "Hombre" else (1.58, 1.51)
                f_min_200, f_max_200 = (1.96, 2.06) if genero == "Hombre" else (1.98, 2.08)
                proyecciones_rango["60m"] = (tiempo_neutral / f_min_60, tiempo_neutral / f_max_60)
                proyecciones_rango["200m"] = (tiempo_neutral * f_min_200, tiempo_neutral * f_max_200)
                
            elif distancia == "200m":
                f_min_100, f_max_100 = (2.06, 1.96) if genero == "Hombre" else (2.08, 1.98)
                f_min_400, f_max_400 = (2.15, 2.25) if genero == "Hombre" else (2.20, 2.30)
                proyecciones_rango["100m"] = (tiempo_neutral / f_min_100, tiempo_neutral / f_max_100)
                proyecciones_rango["400m"] = (tiempo_neutral * f_min_400, tiempo_neutral * f_max_400)

            elif distancia == "400m":
                f_min_200, f_max_200 = (2.25, 2.15) if genero == "Hombre" else (2.30, 2.20)
                proyecciones_rango["200m"] = (tiempo_neutral / f_min_200, tiempo_neutral / f_max_200)
                
            # Mostrar las proyecciones
            if proyecciones_rango:
                p_cols = st.columns(len(proyecciones_rango))
                for idx, (dist, (t_min, t_max)) in enumerate(proyecciones_rango.items()):
                    p_cols[idx].metric(
                        label=f"Rango Estimado en {dist}", 
                        value=f"{t_min:.2f}s - {t_max:.2f}s",
                        help="El tiempo rápido simula un perfil resistente; el lento un perfil explosivo."
                    )
            else:
                st.write("Proyecciones no disponibles para este cruce de datos.")
                
            st.markdown("---")
            
            # 4. Tabla de Simulación Automática
            st.subheader("📊 Tabla de Simulación de Vientos")
            if distancia == "400m":
                st.write("Nota: Al ser una prueba de vuelta completa al anillo, las variaciones de viento lineal en la recta principal no alteran el cómputo oficial de manera significativa:")
                vientos_simular = [0.0]
            else:
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
            
            # 5. Cuadro "Copiar para WhatsApp" (ESTRUCTURA ORIGINAL INTACTA)
            st.subheader("📱 Compartir con el Equipo")
            st.write("Haz clic en el botón de copiar (icono de dos cuadraditos) para pegarlo en WhatsApp:")
            
            texto_proyecciones_wa = ""
            for dist, (t_min, t_max) in proyecciones_rango.items():
                texto_proyecciones_wa += f"🎯 *Rango {dist}:* {t_min:.2f}s a {t_max:.2f}s\n"

            # Formato de variables adaptado a 400m o resto de pruebas
            txt_viento = f" (Viento: {viento:+} m/s)" if distancia != "400m" else ""
            txt_neutral = "Tiempo Neutral (0.0)" if distancia != "400m" else "Tiempo Neutral"

            texto_whatsapp = (
                f"🏃‍♂️ *¡Resultado de la Calculadora de Viento!*\n"
                f"🏁 *Prueba:* {distancia} ({genero})\n"
                f"⏱️ *Tiempo Real:* {tiempo_real:.2f}s{txt_viento}\n"
                f"✨ *{txt_neutral}:* {tiempo_neutral:.2f}s\n"
                f"🚦 *Estado:* {estado_legal}\n\n"
                f"🏆 *Estatus de Mínima:*\n"
                f"{texto_minimas_wa}\n\n"
            )
            
            # Añadir proyecciones sólo si existen
            if texto_proyecciones_wa:
                texto_whatsapp += f"🔮 *Ventana de Potencial Estimado:*\n{texto_proyecciones_wa}"
                
            st.code(texto_whatsapp.strip(), language="text")


# ==========================================
# PESTAÑA 2: COMPARADOR CARA A CARA (DUELO VIRTUAL)
# ==========================================
with tab2:
    st.header("⚔️ Duelo Virtual de Atletas")
    st.write("¿Quién ha sido realmente más rápido? Compara a dos atletas que corrieron en series diferentes con vientos distintos.")
    
    duelo_distancia = st.selectbox("Selecciona la distancia del duelo:", ["60m", "100m", "200m", "400m"], index=1)
    
    col_at1, col_at2 = st.columns(2)
    
    with col_at1:
        st.markdown("### 🏃‍♂️ Atleta 1")
        nom1 = st.text_input("Nombre Atleta 1:", value="Atleta A")
        t1 = st.number_input("Tiempo registrado (s):", value=None, min_value=0.0, step=0.01, placeholder="Ej: 48.50", key="t1")
        
        # Corrección de caché para 400m
        if duelo_distancia == "400m":
            v1 = st.number_input("Viento medido (m/s):", value=0.0, step=0.1, disabled=True, key="v1_400", help="No aplica en 400m")
        else:
            v1 = st.number_input("Viento medido (m/s):", value=None, step=0.1, placeholder="Ej: +1.5", key="v1")
            
        g1 = st.radio("Género Atleta 1:", ["Hombre", "Mujer"], index=0, key="g1", horizontal=True)
        
    with col_at2:
        st.markdown("### 🏃‍♀️ Atleta 2")
        nom2 = st.text_input("Nombre Atleta 2:", value="Atleta B")
        t2 = st.number_input("Tiempo registrado (s):", value=None, min_value=0.0, step=0.01, placeholder="Ej: 49.10", key="t2")
        
        # Corrección de caché para 400m
        if duelo_distancia == "400m":
            v2 = st.number_input("Viento medido (m/s):", value=0.0, step=0.1, disabled=True, key="v2_400", help="No aplica en 400m")
        else:
            v2 = st.number_input("Viento medido (m/s):", value=None, step=0.1, placeholder="Ej: -0.8", key="v2")
            
        g2 = st.radio("Género Atleta 2:", ["Hombre", "Mujer"], index=0, key="g2", horizontal=True)

    if st.button("🔥 ¡Iniciar Duelo Virtual!", type="primary"):
        if t1 is None or v1 is None or t2 is None or v2 is None:
            st.error("⚠️ Es obligatorio rellenar los tiempos de ambos atletas para simular el duelo.")
        else:
            coef1 = obtener_coeficiente(duelo_distancia, g1)
            coef2 = obtener_coeficiente(duelo_distancia, g2)
            
            n1 = t1 + (v1 * coef1)
            n2 = t2 + (v2 * coef2)
            
            st.markdown("### 🏆 Veredicto del Duelo Virtual")
            st.write(f"👉 El tiempo ajustado de **{nom1}** equivale a: **{n1:.2f}s**")
            st.write(f"👉 El tiempo ajustado de **{nom2}** equivale a: **{n2:.2f}s**")
            
            if abs(n1 - n2) < 0.001:
                st.info(f"🤝 **¡Empate técnico absoluto!** En igualdad de condiciones, habrían clavado la misma marca.")
            elif n1 < n2:
                diferencia = n2 - n1
                st.success(f"👑 **¡Ganador Virtual: {nom1}!** Corriendo en las mismas condiciones climáticas, habría aventajado a {nom2} por **{diferencia:.2f}s**.")
            else:
                diferencia = n1 - n2
                st.success(f"👑 **¡Ganador Virtual: {nom2}!** Corriendo en las mismas condiciones climáticas, habría aventajado a {nom1} por **{diferencia:.2f}s**.")
