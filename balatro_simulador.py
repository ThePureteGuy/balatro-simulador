import streamlit as st
import random
from collections import Counter
import matplotlib.pyplot as plt

# -----------------------------
# Baraja estándar
# -----------------------------
palos = ['♠', '♥', '♦', '♣']
valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
baraja = [valor + palo for valor in valores for palo in palos]

# -----------------------------
# Funciones de simulación
# -----------------------------
def generar_mano(baraja, cantidad=5):
    return random.sample(baraja, cantidad)

def obtener_valores(mano):
    return [carta[:-1] for carta in mano]

def evaluar_mano(mano):
    valores = obtener_valores(mano)
    conteo = Counter(valores)
    repeticiones = sorted(conteo.values(), reverse=True)

    if repeticiones == [4, 1]:
        return "Póker"
    elif repeticiones == [3, 2]:
        return "Full House"
    elif repeticiones == [3, 1, 1]:
        return "Trío"
    elif repeticiones == [2, 2, 1]:
        return "Doble Par"
    elif repeticiones == [2, 1, 1, 1]:
        return "Par"
    else:
        return "Carta Alta"

def simular_manos(baraja, repeticiones):
    resultados = {
        "Póker": 0,
        "Full House": 0,
        "Trío": 0,
        "Doble Par": 0,
        "Par": 0,
        "Carta Alta": 0
    }
    manos_guardadas = []

    for _ in range(repeticiones):
        mano = generar_mano(baraja)
        tipo = evaluar_mano(mano)
        resultados[tipo] += 1
        manos_guardadas.append(tuple(mano))  # tupla para poder contar

    # Mano más habitual
    conteo_manos = Counter(manos_guardadas)
    mano_mas_habitual = conteo_manos.most_common(1)[0][0]  # tupla de 5 cartas

    return resultados, mano_mas_habitual

def formatear_mano(mano_tupla):
    # Convierte ('K♣','7♦','A♥','3♠','10♣') en "K♣ 7♦ A♥ 3♠ 10♣"
    return " ".join(mano_tupla)

# -----------------------------
# Interfaz Streamlit
# -----------------------------
st.set_page_config(page_title="Simulación Monte Carlo Balatro", page_icon="🃏", layout="centered")

st.title("Simulación Monte Carlo de manos tipo Balatro")
st.write("Generá miles de manos aleatorias, estimá probabilidades y visualizá la mano más habitual.")

# Controles
col1, col2 = st.columns(2)
with col1:
    repeticiones = st.slider("Cantidad de simulaciones", min_value=100, max_value=20000, step=100, value=2000)
with col2:
    st.write("")

# Ejecutar
if st.button("Ejecutar simulación"):
    resultados, mano_mas_habitual = simular_manos(baraja, repeticiones)

    # Probabilidades
    tipos = list(resultados.keys())
    cantidades = list(resultados.values())
    porcentajes = [c / repeticiones * 100 for c in cantidades]

    st.subheader("Resultados")
    for tipo, cantidad, porcentaje in zip(tipos, cantidades, porcentajes):
        st.write(f"- {tipo}: {cantidad} veces ({porcentaje:.2f}%)")

    # Gráfico
    fig, ax = plt.subplots()
    ax.bar(tipos, porcentajes, color='#5DADE2')
    ax.set_title("Probabilidad estimada por tipo de mano")
    ax.set_ylabel("Probabilidad (%)")
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # Mano más habitual (visual)
    st.subheader("Mano más habitual")
    st.markdown(
        f"""
        <div style="
            border: 2px solid #2ECC71;
            border-radius: 10px;
            padding: 12px;
            background-color: #E8F8F5;
            font-size: 22px;
            text-align: center;
        ">
            <strong>Mano más habitual:</strong><br>
            {formatear_mano(mano_mas_habitual)}
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("Ajustá la cantidad de simulaciones y presioná el botón para ver resultados.")

