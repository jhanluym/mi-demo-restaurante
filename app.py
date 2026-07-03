import streamlit as st
import pandas as pd
import os

# Configuración básica
st.set_page_config(page_title="Sistema Restaurante", layout="wide")

# Carga de datos
archivo_datos = 'inventario.csv'

# Si el archivo no existe, crea una base mínima para que no de error
if not os.path.exists(archivo_datos):
    data = {
        'Plato': ['Ceviche', 'Arroz con Pato', 'Lomo Saltado', 'Seco de Cabrito'],
        'Stock': [5, 2, 0, 5],
        'Precio_Venta': [35.0, 25.0, 40.0, 30.0],
        'Imagen': ['' for _ in range(4)]
    }
    df_inicial = pd.DataFrame(data)
    df_inicial.to_csv(archivo_datos, index=False, sep=';')

# Cargar el CSV
df = pd.read_csv(archivo_datos, sep=';')

# Navegación
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", ["📊 Dashboard", "📦 Inventario", "🍽️ Carta Digital"])

# --- DASHBOARD ---
if opcion == "📊 Dashboard":
    st.title("📊 Panel de Control")
    st.bar_chart(df.set_index('Plato')['Stock'])

# --- INVENTARIO ---
elif opcion == "📦 Inventario":
    st.title("📦 Gestión de Inventario")
    df_edit = st.data_editor(df, use_container_width=True)
    if st.button("Guardar Cambios"):
        df_edit.to_csv(archivo_datos, index=False, sep=';')
        st.success("Guardado exitosamente")
        st.rerun()

# --- CARTA DIGITAL ---
elif opcion == "🍽️ Carta Digital":
    st.title("🍽️ Nuestra Carta")
    st.markdown("---")
    
    for index, row in df.iterrows():
        col1, col2 = st.columns([1, 2])
        
        # Mostrar Imagen
        with col1:
            if pd.notna(row['Imagen']) and str(row['Imagen']).strip() != "":
                try:
                    st.image(row['Imagen'], width=150)
                except:
                    st.write("📷 Imagen no disponible")
            else:
                st.write("📷 Sin foto")
        
        # Mostrar Info
        with col2:
            st.markdown(f"### {row['Plato']}")
            if row['Stock'] > 0:
                st.markdown(f"**Precio: S/ {row['Precio_Venta']:.2f}**")
            else:
                st.markdown("<span style='color:red'>🚫 AGOTADO</span>", unsafe_allow_html=True)
        st.markdown("---")