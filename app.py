import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema Restaurante", layout="wide")

# --- FUNCIONES ---
def registrar_log(mensaje):
    with open('log.txt', "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}\n")

archivo_datos = 'inventario.csv'

# --- CARGA DE DATOS ---
if os.path.exists(archivo_datos):
    df = pd.read_csv(archivo_datos, sep=';')
else:
    data = {
        'Plato': ['Ceviche', 'Arroz con Pato', 'Lomo Saltado'],
        'Stock': [15, 8, 12],
        'Ventas_Semana': [120, 85, 95],
        'Costo': [15.0, 10.0, 18.0],
        'Precio_Venta': [35.0, 25.0, 40.0],
        'Imagen': ['https://via.placeholder.com/150' for _ in range(3)]
    }
    df = pd.DataFrame(data)
    df.to_csv(archivo_datos, index=False, sep=';')

# --- NAVEGACIÓN ---
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", ["📊 Dashboard", "📦 Inventario", "🍽️ Carta Digital"])

# --- DASHBOARD ---
if opcion == "📊 Dashboard":
    st.title("📊 Panel de Control")
    # (Tus métricas aquí)
    st.bar_chart(df.set_index('Plato')['Stock'])

# --- INVENTARIO ---
elif opcion == "📦 Inventario":
    st.title("📦 Gestión de Inventario")
    producto = st.selectbox("Selecciona:", df['Plato'])
    cant = st.number_input("Cantidad:", min_value=1)
    if st.button("➕ Sumar"):
        df.loc[df['Plato'] == producto, 'Stock'] += cant
        df.to_csv(archivo_datos, index=False, sep=';')
        st.rerun()
    df_edit = st.data_editor(df, use_container_width=True)
    if st.button("Guardar Cambios"):
        df_edit.to_csv(archivo_datos, index=False, sep=';')
        st.success("Guardado")
        st.rerun()

# --- CARTA DIGITAL ---
elif opcion == "🍽️ Carta Digital":
    st.title("🍽️ Nuestra Carta")
    st.markdown("---")
    for index, row in df.iterrows():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            try: st.image(row['Imagen'], width=150)
            except: st.write("📷")
        with col2:
            st.markdown(f"### {row['Plato']}")
        with col3:
            if row['Stock'] > 0:
                st.markdown(f"### S/ {row['Precio_Venta']:.2f}")
            else:
                st.markdown("<h3 style='color:red;'>🚫 AGOTADO</h3>", unsafe_allow_html=True)
        st.markdown("---")