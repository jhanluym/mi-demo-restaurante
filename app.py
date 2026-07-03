import streamlit as st
import pandas as pd
import os

# Configuración básica
st.set_page_config(page_title="Menú Restaurante", layout="wide")

# Lógica para ocultar el panel (sidebar) si la URL tiene ?view=cliente
params = st.query_params
is_client = params.get("view") == "cliente"

if is_client:
    st.markdown("""<style>[data-testid="stSidebar"] {display: none !important;}</style>""", unsafe_allow_html=True)

archivo_datos = 'inventario.csv'

# Carga de datos
if not os.path.exists(archivo_datos):
    data = {
        'Plato': ['Ceviche', 'Arroz con Pato', 'Lomo Saltado', 'Seco de Cabrito'],
        'Stock': [5, 2, 0, 5],
        'Precio_Venta': [35.0, 25.0, 40.0, 30.0],
        'Imagen': ['' for _ in range(4)]
    }
    pd.DataFrame(data).to_csv(archivo_datos, index=False, sep=';')

# Cargar CSV forzando que la columna Imagen sea texto
df = pd.read_csv(archivo_datos, sep=';', dtype={'Imagen': str})

# Navegación
if not is_client:
    st.sidebar.title("Navegación")
    opcion = st.sidebar.radio("Ir a:", ["🍽️ Carta Digital", "📊 Dashboard", "📦 Inventario"])
else:
    opcion = "🍽️ Carta Digital"

# --- CONTENIDO ---
if opcion == "🍽️ Carta Digital":
    st.title("🍽️ Nuestra Carta")
    st.markdown("---")
    for index, row in df.iterrows():
        col1, col2 = st.columns([1, 3])
        
        # Definimos la variable correctamente antes de usarla
        img_url = str(row['Imagen']).strip()
        
        with col1:
            # Si el link está vacío, es 'nan', es '0' o no es válido, ponemos la imagen gris
            if img_url in ['nan', '0', '']:
                st.image("https://via.placeholder.com/150", use_container_width=True)
            else:
                try:
                    st.image(img_url, use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/150", use_container_width=True)
        
        with col2:
            st.markdown(f"### {row['Plato']}")
            # Convertimos stock a entero para asegurar comparación
            try:
                stock_val = int(row['Stock'])
            except:
                stock_val = 0
                
            if stock_val > 0:
                st.markdown(f"**Precio: S/ {float(row['Precio_Venta']):.2f}**")
            else:
                st.markdown("<h3 style='color:red;'>🚫 AGOTADO</h3>", unsafe_allow_html=True)
        st.markdown("---")

elif opcion == "📊 Dashboard" and not is_client:
    st.title("📊 Panel de Control")
    st.bar_chart(df.set_index('Plato')['Stock'])

elif opcion == "📦 Inventario" and not is_client:
    st.title("📦 Gestión de Inventario")
    df_edit = st.data_editor(df, use_container_width=True)
    if st.button("Guardar Cambios"):
        df_edit.to_csv(archivo_datos, index=False, sep=';')
        st.success("Guardado")
        st.rerun()