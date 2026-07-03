import streamlit as st
import pandas as pd
import os
import qrcode
from io import BytesIO

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema Restaurante", layout="wide")

# --- DETECCIÓN DE MODO CLIENTE ---
# Si en el link ponemos ?view=cliente, activamos modo oculto
params = st.query_params
is_client = params.get("view") == "cliente"

if is_client:
    # Ocultar menú lateral (Sidebar)
    st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

archivo_datos = 'inventario.csv'

# --- CARGA DE DATOS ---
if os.path.exists(archivo_datos):
    df = pd.read_csv(archivo_datos, sep=';')
else:
    data = {'Plato': ['Ceviche', 'Lomo Saltado'], 'Stock': [10, 10], 'Precio_Venta': [30.0, 35.0], 'Imagen': ['' for _ in range(2)]}
    df = pd.DataFrame(data)
    df.to_csv(archivo_datos, index=False, sep=';')

# --- NAVEGACIÓN ---
if not is_client:
    st.sidebar.title("Navegación")
    opcion = st.sidebar.radio("Ir a:", ["📊 Dashboard", "📦 Inventario", "🍽️ Carta Digital"])
else:
    opcion = "🍽️ Carta Digital"

# --- LÓGICA DE PANTALLAS ---
if opcion == "📊 Dashboard":
    st.title("📊 Panel de Control")
    st.bar_chart(df.set_index('Plato')['Stock'])
    # Generador de QR dentro del dashboard
    st.subheader("🔗 QR para clientes")
    url_cliente = st.text_input("Link de la app:", "https://TU-APP-EN-STREAMLIT.streamlit.app/?view=cliente")
    if st.button("Generar QR"):
        qr = qrcode.make(url_cliente)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf, width=200)

elif opcion == "📦 Inventario":
    st.title("📦 Gestión de Inventario")
    df_edit = st.data_editor(df, use_container_width=True)
    if st.button("Guardar Cambios"):
        df_edit.to_csv(archivo_datos, index=False, sep=';')
        st.success("Guardado exitosamente")
        st.rerun()

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