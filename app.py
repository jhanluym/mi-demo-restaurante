import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema Restaurante", layout="wide")

archivo_datos = 'inventario.csv'

# --- CARGA O CREACIÓN DE DATOS ---
if not os.path.exists(archivo_datos):
    data = {
        'Plato': ['Ceviche', 'Arroz con Pato', 'Lomo Saltado', 'Seco de Cabrito'],
        'Stock': [5, 2, 0, 5],
        'Precio_Venta': [35.0, 25.0, 40.0, 30.0],
        'Imagen': ['' for _ in range(4)]
    }
    df_inicial = pd.DataFrame(data)
    df_inicial.to_csv(archivo_datos, index=False, sep=';')

df = pd.read_csv(archivo_datos, sep=';')

# --- NAVEGACIÓN (Carta primero) ---
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", ["🍽️ Carta Digital", "📊 Dashboard", "📦 Inventario"])

# --- LÓGICA DE CADA SECCIÓN ---

# 1. CARTA DIGITAL
if opcion == "🍽️ Carta Digital":
    st.title("🍽️ Nuestra Carta")
    st.markdown("---")
    for index, row in df.iterrows():
        col1, col2 = st.columns([1, 3])
        with col1:
            try:
                # Si el campo está vacío, pone una imagen gris. Si hay link, intenta cargarla.
                if pd.isna(row['Imagen']) or str(row['Imagen']).strip() == "":
                    st.image("https://via.placeholder.com/150", use_container_width=True)
                else:
                    st.image(row['Imagen'], use_container_width=True)
            except:
                st.image("https://via.placeholder.com/150", use_container_width=True)
        
        with col2:
            st.markdown(f"### {row['Plato']}")
            if row['Stock'] > 0:
                st.markdown(f"**Precio: S/ {row['Precio_Venta']:.2f}**")
            else:
                st.markdown("<h3 style='color:red;'>🚫 AGOTADO</h3>", unsafe_allow_html=True)
        st.markdown("---")

# 2. DASHBOARD
elif opcion == "📊 Dashboard":
    st.title("📊 Panel de Control")
    st.bar_chart(df.set_index('Plato')['Stock'])

# 3. INVENTARIO
elif opcion == "📦 Inventario":
    st.title("📦 Gestión de Inventario")
    df_edit = st.data_editor(df, use_container_width=True)
    if st.button("Guardar Cambios"):
        df_edit.to_csv(archivo_datos, index=False, sep=';')
        st.success("Guardado exitosamente")
        st.rerun()