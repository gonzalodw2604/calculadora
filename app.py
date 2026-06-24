import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Calculadora de Viento PRO", page_icon="🏃‍♂️", layout="centered")

# Base de datos 2026 actualizada con 400m y categorías Master
MINIMAS_DB = {
    "Hombre": {
        "100m": {"Absoluto": 10.55, "Sub23": 10.80, "Sub20": 10.90, "Sub18": 11.10, "Sub16": 11.50, "M35": 11.31, "M40": 11.70, "M45": 11.85, "M50": 12.04, "M55": 12.42, "M60": 12.93},
        "200m": {"Absoluto": 21.30, "Sub23": 21.80, "Sub20": 22.10, "Sub18": 22.60, "M35": 23.02, "M40": 23.60, "M45": 24.07, "M50": 24.69, "M55": 25.78, "M60": 27.04},
        "300m": {"Sub16": 37.00},
        "400m": {"Absoluto": 47.00, "Sub23": 48.00, "Sub20": 49.25, "Sub18": 49.75, "M35": 51.15, "M40": 53.17, "M45": 53.14, "M50": 56.14, "M55": 57.97, "M60": 61.82}
    },
    "Mujer": {
        "100m": {"Absoluto": 11.80, "Sub23": 12.10, "Sub20": 12.30, "Sub18": 12.30, "Sub16": 12.55, "F35": 13.08, "F40": 13.49, "F45": 13.76, "F50": 13.98, "F55": 14.67, "F60": 15.10},
        "200m": {"Absoluto": 24.25, "Sub23": 25.00, "Sub20": 25.25, "Sub18": 25.25, "F35": 26.42, "F40": 27.95, "F45": 28.56, "F50": 28.60, "F55":
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
cat_lista = ["Absoluto", "Sub23", "Sub20", "Sub18", "Sub16", "M35", "M40", "M45"]
categoria_elegida = st.selectbox("Categoría:", cat_lista)

if st.button("🚀 Calcular"):
    coef = obtener_coeficiente(distancia, genero)
    t_neutral = tiempo_real + (viento * coef)
    
    st.write(f"### Tiempo neutral: **{t_neutral:.2f}s**")
    
    # Lógica de Mínimas
    if categoria_elegida in MINIMAS_DB[genero][distancia]:
        minima = MINIMAS_DB[genero][distancia][categoria_elegida]
        diff = t_neutral - minima
        if diff <= 0:
            st.success(f"🎉 ¡Mínima conseguida para el {categoria_elegida}! (Te sobran {abs(diff):.2f}s)")
        else:
            st.warning(f"🎯 Estás a {diff:.2f}s de la mínima de {minima:.2f}s")
    else:
        st.error("Prueba no disponible para esta categoría.")

    st.subheader("🔮 Potencial (Rango Estimado)")
    st.info("El rango muestra tu proyección según si eres un atleta más veloz o más resistente.")
    # (Aquí mantendrías la lógica de rangos anterior para 60, 100, 200 y 400)
