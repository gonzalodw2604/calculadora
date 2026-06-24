import streamlit as st

# Configuración de la pestaña del navegador
st.set_page_config(page_title="Calculadora de Viento para TheBalasTeam", page_icon="🏃‍♂️", layout="centered")

# Título principal de la página web
st.title("🏃‍♂️ Calculadora de Viento Neutral para TheBalasTeam 🏃‍♂️")
st.write("Introduce los datos de tu carrera para calcular el tiempo equivalente con viento cero (0.0 m/s).")

st.markdown("---")

# Crear el formulario con campos que arrancan vacíos para mayor limpieza
distancia = st.selectbox("Selecciona la distancia:", ["60m", "100m", "200m"], index=None, placeholder="Elige una prueba...")
tiempo_real = st.number_input("Tiempo registrado (segundos):", value=None, min_value=0.0, step=0.01, placeholder="Ej: 11.28")
viento = st.number_input("Viento medido (m/s):", value=None, step=0.1, placeholder="Ej: +2.0 o -1.5")
genero = st.radio("Género del atleta:", ["Hombre", "Mujer"], index=None)

st.markdown("---")

# Botón para ejecutar el cálculo
if st.button("Calcular tiempo neutral", type="primary"):
    # Control de seguridad: verificar que no falte ningún dato
    if distancia is None or tiempo_real is None or viento is None or genero is None:
        st.error("⚠️ Por favor, rellena todos los campos antes de calcular.")
    else:
        # Asignación de coeficientes según tu fórmula original
        if distancia == "60m":
            coeficiente = 0.030 if genero == "Hombre" else 0.025
        elif distancia == "100m":
            coeficiente = 0.055 if genero == "Hombre" else 0.050
        elif distancia == "200m":
            coeficiente = 0.090 if genero == "Hombre" else 0.080
        else:
            coeficiente = 0.0
            
        # Cálculo del tiempo corregido
        tiempo_neutral = tiempo_real + (viento * coeficiente)
        
        # Mostrar el resultado final en un cuadro verde elegante
        st.success(f"✨ **Tu tiempo con viento neutral (0.0) sería: {round(tiempo_neutral, 2)}s** ✨")
        
        # Desglose de los datos introducidos para el usuario
        st.info(f"""
        **Resumen de la prueba:**
        * 🏃‍♂️ **Prueba:** {distancia} ({genero})
        * ⏱️ **Tiempo Registrado:** {tiempo_real}s
        * 💨 **Viento:** {viento:+} m/s
        """)
