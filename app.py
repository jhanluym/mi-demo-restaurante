import streamlit as st
import pandas as pd
import os
import qrcode
from io import BytesIO

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Menú Restaurante", layout="wide")

# --- LÓGICA DE VISUALIZACIÓN ---
# Si la URL termina en ?view=cliente, ocultamos todo y mostramos solo la carta
is_client = st.query_params.get("view") == "cliente"

if is_client:
    st.markdown("""<style>[data-testid="stSidebar"] {display: none !important;}</style>""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
archivo_datos = 'inventario.csv'
if os.path.exists(archivo_datos):
    df = pd.read_csv(archivo_datos, sep=';')
else:
    df = pd.DataFrame({'Plato': ['Ceviche'], 'Stock': [10], 'Precio_Venta': [30.0], 'Imagen': ['']})

# --- NAVEGACIÓN ---
if not is_client:
    st.sidebar.title("Navegación")
    opcion = st.sidebar.radio("Ir a:", ["📊 Dashboard", "📦 Inventario", "🍽️ Carta Digital"])
else:
    opcion = "🍽️ Carta Digital"

# --- CONTENIDO ---
if opcion == "📊 Dashboard":
    st.title("📊 Panel de Control")
    # URL para copiar
    url_base = st.text_input("Copia este link para tu QR:", value=f"{st.query_params.get('url', '')}?view=cliente")
    st.info("⚠️ COPIA el link que sale arriba (asegúrate de que tenga ?view=cliente al final) y pégalo en cualquier generador de QR gratuito.")
    
elif opcion == "📦 Inventario":
    st.title("📦 Gestión de Inventario")
    df_edit = st.data_editor(df, use_container_width=True)
    if st.button("Guardar"):
        df_edit.to_csv(archivo_datos, index=False, sep=';')
        st.success("Guardado")
        st.rerun()

elif opcion == "🍽️ Carta Digital":
    st.title("🍽️ Nuestra Carta")
    for index, row in df.iterrows():
        col1, col2 = st.columns([1, 2])
        with col1:
            try: st.image(row['Imagen'], width=100)
            except: st.write("📷")
        with col2:
            st.markdown(f"### {row['Plato']}")
            if row['Stock'] > 0:
                st.markdown(f"**S/ {row['Precio_Venta']:.2f}**")
            else:
                st.markdown("<span style='color:red'>🚫 AGOTADO</span>", unsafe_allow_html=True)
        st.markdown("---")