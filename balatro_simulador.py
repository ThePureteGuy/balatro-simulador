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
    repeticiones = list(conteo.values())

    tiene_par = 2 in repeticiones
    cantidad_pares = repeticiones.count(2)
    tiene_trio = 3 in repeticiones
    tiene_poker = 4 in repeticiones

    if tiene_poker:
        return "Póker"
    elif tiene_trio and tiene_par:
        return "Full House"
    elif tiene_trio:
        return "Trío"
    elif cantidad_pares >= 2:
        return "Doble Par"
    elif tiene_par:
        return "Par"
    else:
        return "Carta Alta"

def simular_manos(baraja, repeticiones, cantidad_cartas=5):
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
        mano = generar_mano(baraja, cantidad=cantidad_cartas)
        tipo = evaluar_mano(mano)
        resultados[tipo] += 1
        manos_guardadas.append(tuple(mano))

    conteo_manos = Counter(manos_guardadas)
    mano_mas_habitual = conteo_manos.most_common(1)[0][0]

    return resultados, mano_mas_habitual

# -----------------------------
# Función para colorear cartas según palo
# -----------------------------
def colorear_mano_por_palo(mano):
    salida = []
    for carta in mano:
        palo = carta[-1]  # último carácter es el palo
        if palo in ['♠', '♣']:
            salida.append(f"<span style='color:black'>{carta}</span>")
        elif palo in ['♦', '♥']:
            salida.append(f"<span style='color:red'>{carta}</span>")
        else:
            salida.append(carta)
    return " ".join(salida)

# -----------------------------
# Interfaz Streamlit
# -----------------------------
st.set_page_config(page_title="Simulación Monte Carlo Balatro", page_icon="🃏", layout="centered")

st.title("Simulación Monte Carlo de manos tipo Balatro")
st.write("Generá miles de manos aleatorias, estimá probabilidades y visualizá la mano más habitual con colores reales de los palos.")

# Controles
repeticiones = st.slider("Cantidad de simulaciones", min_value=100, max_value=20000, step=100, value=2000)

# Ejecutar
if st.button("Ejecutar simulación"):
    # Simulación estándar (5 cartas)
    resultados_5, mano_mas_habitual_5 = simular_manos(baraja, repeticiones, cantidad_cartas=5)

    # Simulación Balatro PC (8 cartas)
    resultados_8, mano_mas_habitual_8 = simular_manos(baraja, repeticiones, cantidad_cartas=8)

    # Probabilidades 5 cartas
    st.subheader("Resultados (5 cartas)")
    tipos_5 = list(resultados_5.keys())
    cantidades_5 = list(resultados_5.values())
    porcentajes_5 = [c / repeticiones * 100 for c in cantidades_5]
    for tipo, cantidad, porcentaje in zip(tipos_5, cantidades_5, porcentajes_5):
        st.write(f"- {tipo}: {cantidad} veces ({porcentaje:.2f}%)")

    # Gráfico 5 cartas
    fig5, ax5 = plt.subplots()
    ax5.bar(tipos_5, porcentajes_5, color='#5DADE2')
    ax5.set_title("Probabilidad estimada por tipo de mano (5 cartas)")
    ax5.set_ylabel("Probabilidad (%)")
    ax5.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig5)

    # Mano más habitual (5 cartas)
    st.subheader("Mano más habitual (5 cartas)")
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
            {colorear_mano_por_palo(mano_mas_habitual_5)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Probabilidades 8 cartas (Balatro PC)
    st.subheader("Resultados (Balatro PC - 8 cartas)")
    tipos_8 = list(resultados_8.keys())
    cantidades_8 = list(resultados_8.values())
    porcentajes_8 = [c / repeticiones * 100 for c in cantidades_8]
    for tipo, cantidad, porcentaje in zip(tipos_8, cantidades_8, porcentajes_8):
        st.write(f"- {tipo}: {cantidad} veces ({porcentaje:.2f}%)")

    # Gráfico 8 cartas
    fig8, ax8 = plt.subplots()
    ax8.bar(tipos_8, porcentajes_8, color='#F5B041')
    ax8.set_title("Probabilidad estimada por tipo de mano (Balatro PC - 8 cartas)")
    ax8.set_ylabel("Probabilidad (%)")
    ax8.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig8)

    # Mano más habitual (Balatro PC - 8 cartas)
    st.subheader("Mano más habitual (Balatro PC - 8 cartas)")
    st.markdown(
        f"""
        <div style="
            border: 2px solid #F39C12;
            border-radius: 10px;
            padding: 12px;
            background-color: #FEF5E7;
            font-size: 22px;
            text-align: center;
        ">
            <strong>Mano más habitual (Balatro PC):</strong><br>
            {colorear_mano_por_palo(mano_mas_habitual_8)}
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("Ajustá la cantidad de simulaciones y presioná el botón para ver resultados.")
