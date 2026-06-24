import streamlit as st
import pandas as pd

# Configuración de la pestaña del navegador
st.set_page_config(page_title="Calculadora de Viento PRO", page_icon="🏃‍♂️", layout="centered")

# Base de datos interna con marcas mínimas oficiales de referencia (RFEA aproximadas PC/AL)
# ¡Actualizada con categorías Máster de 35 a 55 años!
MINIMAS_DB = {
    "Hombre": {
        "60m": {"Absoluto": 6.85, "Sub23": 6.95, "Sub20": 7.05, "Sub18": 7.15, "Sub16": 7.35, "Máster 35": 7.30, "Máster 40": 7.55, "Máster 45": 7.60, "Máster 50": 7.70, "Máster 55": 8.20},
        "100m": {"Absoluto": 10.65, "Sub23": 10.90, "Sub20": 11.15, "Sub18": 11.35, "Sub16": 11.60, "Máster 35": 11.50, "Máster 40": 11.90, "Máster 45": 12.00, "Máster 50": 12.50, "Máster 55": 13.00},
        "200m": {"Absoluto": 21.60, "Sub23": 22.10, "Sub20": 22.55, "Sub18": 22.95, "Máster 35": 23.20, "Máster 40": 24.50, "Máster 45": 24.50, "Máster 50": 25.50, "Máster 55": 26.50},
        "400m": {"Absoluto": 48.00, "Sub23": 48.90, "Sub20": 49.75, "Sub18": 50.95, "Máster 35": 52.00, "Máster 40": 54.00, "Máster 45": 55.00, "Máster 50": 57.50, "Máster 55": 59.80}
    },
    "Mujer": {
        "60m": {"Absoluto": 7.65, "Sub23": 7.85, "Sub20": 7.95, "Sub18": 8.05, "Sub16": 8.20, "Máster 35": 8.70, "Máster 40": 8.80, "Máster 45": 8.90, "Máster 50": 9.10, "Máster 55": 9.50},
        "100m": {"Absoluto": 11.95, "Sub23": 12.30, "Sub20": 12.60, "Sub18": 12.75, "Sub16": 12.90, "Máster 35": 14.00, "Máster 40": 14.00, "Máster 45": 14.00, "Máster 50": 14.70, "Máster 55": 15.40},
        "200m": {"Absoluto": 24.45, "Sub23": 25.30, "Sub20": 25.80, "Sub18": 26.30, "Máster 35": 28.30, "Máster 40": 28.50, "Máster 45": 29.00, "Máster 50": 29.80, "Máster 55": 32.00},
        "400m": {"Absoluto": 55.00, "Sub23": 56.80, "Sub20": 57.75, "Sub18": 59.25, "Máster 35": 62.50, "Máster 40": 64.00, "Máster 45": 64.00, "Máster 50": 68.00, "Máster 55": 69.00}
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
st.title("🏃‍♂️ Calculadora de Viento Neutral PRO 🏃‍♀️")
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
