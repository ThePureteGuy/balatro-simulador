import streamlit as st
import random
from collections import Counter
import matplotlib.pyplot as plt

# Crear baraja
palos = ['♠', '♥', '♦', '♣']
valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
baraja = [valor + palo for valor in valores for palo in palos]

# Funciones
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
    for _ in range(repeticiones):
        mano = generar_mano(baraja)
        tipo = evaluar_mano(mano)
        resultados[tipo] += 1
    return resultados

# Interfaz Streamlit
st.title("Simulación Monte Carlo de manos tipo Balatro")
st.write("Este simulador genera manos aleatorias y calcula la probabilidad de cada tipo.")

repeticiones = st.slider("Cantidad de simulaciones", min_value=100, max_value=10000, step=100, value=1000)

if st.button("Ejecutar simulación"):
    resultados = simular_manos(baraja, repeticiones)
    tipos = list(resultados.keys())
    cantidades = list(resultados.values())
    porcentajes = [c / repeticiones * 100 for c in cantidades]

    st.subheader("Resultados")
    for tipo, cantidad, porcentaje in zip(tipos, cantidades, porcentajes):
        st.write(f"{tipo}: {cantidad} veces ({porcentaje:.2f}%)")

    # Gráfico
    fig, ax = plt.subplots()
    ax.bar(tipos, porcentajes, color='skyblue')
    ax.set_title("Probabilidad estimada por tipo de mano")
    ax.set_ylabel("Probabilidad (%)")
    st.pyplot(fig)
