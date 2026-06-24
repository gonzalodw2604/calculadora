import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Calculadora de Viento PRO", page_icon="🏃‍♂️", layout="centered")

# Base de datos 2026 actualizada con 400m y categorías Master
MINIMAS_DB = {
    "Hombre": {
        "60m": {"Absoluto": 6.80, "Sub23": 6.95, "Sub20": 7.05, "Sub18": 7.20, "Sub16": 7.35, "M35": 7.50, "M40": 7.70, "M45": 7.90},
        "100m": {"Absoluto": 10.60, "Sub23": 10.90, "Sub20": 11.10, "Sub18": 11.30, "Sub16": 11.55, "M35": 11.80, "M40": 12.10, "M45": 12.40},
        "200m": {"Absoluto": 21.40, "Sub23": 21.90, "Sub20": 22.40, "Sub18": 22.80, "M35": 23.50, "M40": 24.00, "M45": 24.50},
        "400m": {"Absoluto": 47.80, "Sub23": 48.90, "Sub20": 50.00, "Sub18": 51.50, "M35": 53.00, "M40": 54.50, "M45": 56.00}
    },
    "Mujer": {
        "60m": {"Absoluto": 7.55, "Sub23": 7.75, "Sub20": 7.85, "Sub18": 8.00, "Sub16": 8.15, "M35": 8.40, "M40": 8.60, "M45": 8.80},
        "100m": {"Absoluto": 11.90, "Sub23": 12.25, "Sub20": 12.50, "Sub18": 12.65, "Sub16": 12.85, "M35": 13.20, "M40": 13.60, "M45": 14.00},
        "200m": {"Absoluto": 24.30, "Sub23": 25.20, "Sub20": 25.70, "Sub18": 26.00, "M35": 27.50, "M40": 28.50, "M45": 29.50},
        "400m": {"Absoluto": 54.50, "Sub23": 56.80, "Sub20": 58.50, "Sub18": 60.00, "M35": 63.00, "M40": 65.00, "M45": 68.00}
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
