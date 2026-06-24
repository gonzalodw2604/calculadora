import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Calculadora de Viento PRO", page_icon="🏃‍♂️", layout="centered")

# Base de datos 2026 actualizada con imagen oficial (M35-M60, F35-F60 y nuevas Sub23)
MINIMAS_DB = {
    "Hombre": {
        "100m": {"Absoluto": 10.55, "Sub23": 10.75, "Sub20": 10.90, "Sub18": 11.10, "Sub16": 11.50, "M35": 11.31, "M40": 11.70, "M45": 11.85, "M50": 12.04, "M55": 12.42, "M60": 12.93},
        "200m": {"Absoluto": 21.30, "Sub23": 21.75, "Sub20": 22.10, "Sub18": 22.60, "M35": 23.02, "M40": 23.60, "M45": 24.07, "M50": 24.69, "M55": 25.78, "M60": 27.04},
        "300m": {"Sub16": 37.00},
        "400m": {"Absoluto": 47.00, "Sub23": 48.00, "Sub20": 49.25, "Sub18": 49.75, "M35": 51.15, "M40": 53.17, "M45": 53.14, "M50": 56.14, "M55": 57.97, "M60": 61.82}
    },
    "Mujer": {
        "100m": {"Absoluto": 11.80, "Sub23": 12.05, "Sub20": 12.30, "Sub18": 12.30, "Sub16": 12.55, "F35": 13.08, "F40": 13.49, "F45": 13.76, "F50": 13.98, "F55": 14.67, "F60": 15.10},
        "200m": {"Absoluto": 24.25, "Sub23": 24.85, "Sub20": 25.25, "Sub18": 25.25, "F35": 26.42, "F40": 27.95, "F45": 28.56, "F50": 28.60, "F55": 30.19, "F60": 32.06},
        "400m": {"Sub23": 56.25, "F35": 61.15, "F40": 62.69, "F45": 64.29, "F50": 65.95, "F55": 68.18, "F60": 74.29}
    }
}

def obtener_coeficiente(distancia, genero):
    # Nota: El viento afecta menos al 400m por la curva, se usa un coeficiente reducido
    if distancia == "60m": return 0.030 if genero == "Hombre" else 0.025
    if distancia == "100m": return 0.055 if genero == "Hombre" else 0.050
    if distancia == "200m": return 0.090 if genero == "Hombre" else 0.080
    if distancia == "400m": return 0.120 if genero == "Hombre" else 0.110
    return 0.0

st.title("🏃‍♂️ Calculadora de Viento PRO 2026")

# Layout de inputs
col1, col2 = st.columns(2)
with col1:
    distancia = st.selectbox("Distancia:", ["60m", "100m", "200m", "400m"])
    tiempo_real = st.number_input("Tiempo (s):", min_value=0.0, step=0.01)
with col2:
    viento = st.number_input("Viento (m/s):", step=0.1)
    genero = st.radio("Género:", ["Hombre", "Mujer"], horizontal=True)

# Selector de categoría dinámico
cat_lista = ["Absoluto", "Sub23", "Sub20", "Sub18", "Sub16", "M35", "M40", "M45", "M50", "M55", "M60", "F35", "F40", "F45", "F50", "F55", "F60"]
categoria_elegida = st.selectbox("Categoría:", cat_lista)

if st.button("🚀 Calcular"):
    if tiempo_real > 0:
        coef = obtener_coeficiente(distancia, genero)
        
        # El tiempo neutral es el tiempo corregido quitando el efecto del viento
        t_neutral = tiempo_real + (viento * coef)
        
        st.write(f"### Tiempo neutral: **{t_neutral:.2f}s**")
        
        # Lógica de Mínimas con protección por si la distancia no está en la base de datos
        if distancia in MINIMAS_DB[genero] and categoria_elegida in MINIMAS_DB[genero][distancia]:
            minima = MINIMAS_DB[genero][distancia][categoria_elegida]
            diff = t_neutral - minima
            if diff <= 0:
                st.success(f"🎉 ¡Mínima conseguida para la categoría {categoria_elegida}! (Te sobran {abs(diff):.2f}s)")
            else:
                st.warning(f"🎯 Estás a {diff:.2f}s de la mínima de {minima:.2f}s")
        else:
            st.error("Prueba o categoría no disponible en la base de datos para este género.")

        # Lógica de rangos / proyecciones
        st.subheader("🔮 Potencial (Rango Estimado)")
        st.info("El rango muestra tu proyección según si eres un atleta más veloz (explosivo) o más resistente.")
        
        col_res1, col_res2 = st.columns(2)
        
        if distancia == "60m":
            # Proyección a 100m (aprox x1.53 para explosivos, x1.56 para menos veloces al final)
            r_100_min = t_neutral * 1.53
            r_100_max = t_neutral * 1.56
            with col_res1:
                st.metric(label="Proyección 100m", value=f"{r_100_min:.2f} - {r_100_max:.2f}s")

        elif distancia == "100m":
            # Proyección a 60m y 200m
            r_60_min = t_neutral / 1.56
            r_60_max = t_neutral / 1.53
            r_200_min = (t_neutral * 2) - 0.2
            r_200_max = (t_neutral * 2) + 0.4
            with col_res1:
                st.metric(label="Proyección 60m", value=f"{r_60_min:.2f} - {r_60_max:.2f}s")
            with col_res2:
                st.metric(label="Proyección 200m", value=f"{r_200_min:.2f} - {r_200_max:.2f}s")

        elif distancia == "200m":
            # Proyección a 100m y 400m
            r_100_min = (t_neutral - 0.4) / 2
            r_100_max = (t_neutral + 0.2) / 2
            r_400_min = t_neutral * 2.14
            r_400_max = t_neutral * 2.20
            with col_res1:
                st.metric(label="Proyección 100m", value=f"{r_100_min:.2f} - {r_100_max:.2f}s")
            with col_res2:
                st.metric(label="Proyección 400m", value=f"{r_400_min:.2f} - {r_400_max:.2f}s")

        elif distancia == "400m":
            # Proyección a 200m
            r_200_min = t_neutral / 2.20
            r_200_max = t_neutral / 2.14
            with col_res1:
                st.metric(label="Proyección 200m", value=f"{r_200_min:.2f} - {r_200_max:.2f}s")
    else:
        st.warning("Introduce un tiempo válido mayor a 0.")
