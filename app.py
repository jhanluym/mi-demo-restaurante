import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Gestión Restaurante", layout="wide")

# --- FUNCIONES DE SOPORTE ---
def registrar_log(mensaje):
    with open('log.txt', "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}\n")

archivo_datos = 'inventario.csv'

# --- CARGA O CREACIÓN DE DATOS ---
if os.path.exists(archivo_datos):
    df = pd.read_csv(archivo_datos, sep=';', on_bad_lines='skip')
else:
    data = {
        'Plato': ['Ceviche', 'Arroz con Pato', 'Lomo Saltado', 'Seco de Cabrito'],
        'Stock': [15, 8, 12, 5],
        'Ventas_Semana': [120, 85, 95, 60],
        'Costo': [15.0, 10.0, 18.0, 12.0],
        'Precio_Venta': [35.0, 25.0, 40.0, 30.0]
    }
    df = pd.DataFrame(data)
    df.to_csv(archivo_datos, index=False, sep=';')

# Cálculos financieros automáticos
df['Ganancia_x_Plato'] = df['Precio_Venta'] - df['Costo']
df['Ganancia_Total_Semanal'] = df['Ganancia_x_Plato'] * df['Ventas_Semana']

# --- MENÚ LATERAL (NAVEGACIÓN) ---
st.sidebar.title("Menú de Gestión")
opcion = st.sidebar.radio("Selecciona una sección:", ["Dashboard", "Inventario"])

# --- SECCIÓN DASHBOARD ---
if opcion == "Dashboard":
    st.title("📊 Panel de Control: Rentabilidad")
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Alertas de Stock", len(df[df['Stock'] < 7]))
    col_kpi2.metric("Ganancia Total Semanal", f"S/ {df['Ganancia_Total_Semanal'].sum():,.2f}")
    col_kpi3.metric("Plato más Rentable", df.loc[df['Ganancia_x_Plato'].idxmax(), 'Plato'])
    
    st.subheader("📈 Rentabilidad por Plato")
    st.bar_chart(df.set_index('Plato')['Ganancia_x_Plato'])

# --- SECCIÓN INVENTARIO ---
elif opcion == "Inventario":
    st.title("📦 Control de Inventario y Costos")
    
    # Acciones rápidas
    st.subheader("⚙️ Acciones Rápidas")
    col1, col2, col3 = st.columns(3)
    producto_seleccionado = col1.selectbox("Selecciona un plato:", df['Plato'])
    cantidad = col2.number_input("Cantidad:", min_value=1, step=1)

    if col3.button("➕ Sumar Stock"):
        df.loc[df['Plato'] == producto_seleccionado, 'Stock'] += cantidad
        df.to_csv(archivo_datos, index=False, sep=';')
        registrar_log(f"SUMA: {cantidad} unidades de {producto_seleccionado}")
        st.rerun()

    if col3.button("➖ Restar Stock"):
        df.loc[df['Plato'] == producto_seleccionado, 'Stock'] -= cantidad
        df.to_csv(archivo_datos, index=False, sep=';')
        registrar_log(f"RESTA: {cantidad} unidades de {producto_seleccionado}")
        st.rerun()

    # Editor de tabla
    st.subheader("Editar Datos Financieros")
    df_editado = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("Guardar Cambios Manuales"):
        df_editado['Ganancia_x_Plato'] = df_editado['Precio_Venta'] - df_editado['Costo']
        df_editado['Ganancia_Total_Semanal'] = df_editado['Ganancia_x_Plato'] * df_editado['Ventas_Semana']
        df_editado.to_csv(archivo_datos, index=False, sep=';')
        registrar_log("Cambio manual en tabla de inventario")
        st.success("¡Datos financieros guardados!")
        st.rerun()

    # Descarga
    csv = df_editado.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button("📥 Descargar Reporte CSV", data=csv, file_name='reporte_inventario.csv', mime='text/csv')