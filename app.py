import streamlit as st
import pandas as pd
import json
import os

# Configuración de página
st.set_page_config(page_title="Control de Barra Pro", layout="wide")

# --- FUNCIONES PARA GUARDAR EN ARCHIVO FÍSICO ---
ARCHIVO_MEMORIA = 'memoria_barra.json'

def cargar_datos():
    # Si el archivo existe, lee lo que se guardó anteriormente
    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar_datos(datos):
    # Escribe los datos actuales en el archivo para que no se borren al cerrar
    with open(ARCHIVO_MEMORIA, 'w') as f:
        json.dump(datos, f)

# --- GESTIÓN DE MEMORIA BLINDADA ---
if 'licores' not in st.session_state:
    st.session_state['licores'] = {
        'Tanqueray': {'oz_botella': 22, 'oz_trago': 2.0},
        'Ron': {'oz_botella': 24, 'oz_trago': 2.0}
    }

# Aquí ahora cargamos desde el archivo físico en lugar de empezar de cero
if 'datos' not in st.session_state:
    st.session_state['datos'] = cargar_datos()

st.title("🍸 App de Control de Inventario")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Configuración")
    if st.button("🔄 REINICIAR TURNO (Borrar Todo)"):
        st.session_state['datos'] = {}
        guardar_datos({}) # Borra el archivo físico también
        st.rerun()

    st.divider()
    st.markdown("**➕ Agregar Nuevo Licor**")
    nuevo_nombre = st.text_input("Nombre del Licor")
    nueva_oz_bot = st.number_input("OZ por botella", value=22)
    if st.button("Agregar Licor"):
        if nuevo_nombre != "":
            st.session_state['licores'][nuevo_nombre] = {'oz_botella': nueva_oz_bot, 'oz_trago': 2.0}
            st.rerun()
            
    st.divider()
    st.markdown("**🗑️ Eliminar Existente**")
    licor_a_eliminar = st.selectbox("Selecciona para borrar", list(st.session_state['licores'].keys()))
    if st.button("Eliminar Licor"):
        if len(st.session_state['licores']) > 1:
            del st.session_state['licores'][licor_a_eliminar]
            if licor_a_eliminar in st.session_state['datos']:
                del st.session_state['datos'][licor_a_eliminar]
                guardar_datos(st.session_state['datos']) # Actualiza el archivo al eliminar
            st.rerun()
        else:
            st.error("Debe quedar al menos 1 licor.")

# --- SELECCIÓN Y LÓGICA ---
licor_seleccionado = st.selectbox("Selecciona el Licor a cuadrar", list(st.session_state['licores'].keys()))
config = st.session_state['licores'][licor_seleccionado]

# Asegurar persistencia del diccionario de datos
if licor_seleccionado not in st.session_state['datos']:
    st.session_state['datos'][licor_seleccionado] = {
        'ib': 0, 'io': 0, 'inb': 0, 'ino': 0, 'sb': 0, 'so': 0,
        'ba': 0, 'vb': 0, 'vt': 0, 'cb': 0, 'ct': 0, 'tb': 0, 'tt': 0, 'pb': 0
    }

d = st.session_state['datos'][licor_seleccionado]

st.markdown(f"<h3 style='text-align: center; color: #4CAF50;'>--- OPERACIÓN: {licor_seleccionado.upper()} ---</h3>", unsafe_allow_html=True)

# --- INTERFAZ EN BLOQUES ---
col_izq, col_der = st.columns(2)

with col_izq:
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>INICIO</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['ib'] = c1.number_input("Botellas", value=int(d['ib']), key=f"ib_{licor_seleccionado}")
        d['io'] = c2.number_input("OZ", value=int(d['io']), key=f"io_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>INGRESO</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['inb'] = c1.number_input("Botellas", value=int(d['inb']), key=f"inb_{licor_seleccionado}")
        d['ino'] = c2.number_input("OZ", value=int(d['ino']), key=f"ino_{licor_seleccionado}")

    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>SALIDA</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['sb'] = c1.number_input("Botellas", value=int(d['sb']), key=f"sb_{licor_seleccionado}")
        d['so'] = c2.number_input("OZ", value=int(d['so']), key=f"so_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>BOT ABIERTA PARA COCTEL</h4>", unsafe_allow_html=True)
        d['ba'] = st.number_input("Botellas a abrir", value=int(d['ba']), key=f"ba_{licor_seleccionado}")

with col_der:
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>VENTA</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['vb'] = c1.number_input("Botellas", value=int(d['vb']), key=f"vb_{licor_seleccionado}")
        d['vt'] = c2.number_input("Tragos", value=int(d['vt']), key=f"vt_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>CORTESÍA</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['cb'] = c1.number_input("Botellas", value=int(d['cb']), key=f"cb_{licor_seleccionado}")
        d['ct'] = c2.number_input("Tragos", value=int(d['ct']), key=f"ct_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>TICKETS</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['tb'] = c1.number_input("Botellas", value=int(d['tb']), key=f"tb_{licor_seleccionado}")
        d['tt'] = c2.number_input("Tragos", value=int(d['tt']), key=f"tt_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>PUERTA</h4>", unsafe_allow_html=True)
        d['pb'] = st.number_input("Botellas Cerradas", value=int(d['pb']), key=f"pb_{licor_seleccionado}")

# --- LÓGICA FINAL ---
final_bot = d['ib'] + d['inb'] - d['sb'] - d['ba'] - d['vb'] - d['cb'] - d['tb'] - d['pb']
total_oz_salida_tragos = (d['vt'] + d['ct'] + d['tt']) * config['oz_trago']
final_oz = (d['io'] + d['ino'] + (d['ba'] * config['oz_botella'])) - d['so'] - total_oz_salida_tragos

st.divider()
with st.container(border=True):
    st.markdown("<h2 style='text-align: center; color: #E74C3C;'>CUADRE FINAL</h2>", unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns([1, 2, 2, 1])
    r2.metric("Botellas", int(final_bot))
    r3.metric("Onzas", int(final_oz))

# --- CUADRO RESUMEN LIMPIO ---
st.markdown("### 📊 Resumen del Desglose")
resumen_data = {
    "Concepto": ["Inicio", "Ingresos", "Salida", "Bot. Abiertas", 
                 f"Salida Botellas (Ven: {d['vb']} | Cor: {d['cb']} | Tic: {d['tb']} | Pta: {d['pb']})", 
                 f"Salida Tragos (Ven: {d['vt']} | Cor: {d['ct']} | Tic: {d['tt']})"],
    "Botellas": [d['ib'], d['inb'], -d['sb'], -d['ba'], -(d['vb'] + d['cb'] + d['tb'] + d['pb']), "-"],
    "Onzas": [d['io'], d['ino'], -d['so'], (d['ba'] * config['oz_botella']), "-", -total_oz_salida_tragos]
}
st.table(pd.DataFrame(resumen_data))

# --- AUTO-GUARDADO FINAL ---
# Esta línea garantiza que cualquier número que cambies se guarde al instante en el archivo
guardar_datos(st.session_state['datos'])
