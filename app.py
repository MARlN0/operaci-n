import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Control de Barra Pro", layout="wide")

st.title("🍸 App de Control de Inventario")

# --- GESTIÓN DE MEMORIA (BAÚL DE DATOS) ---
if 'licores' not in st.session_state:
    st.session_state['licores'] = {
        'Tanqueray': {'oz_botella': 22, 'oz_trago': 2.0},
        'Ron': {'oz_botella': 24, 'oz_trago': 2.0}
    }

if 'datos' not in st.session_state:
    st.session_state['datos'] = {}

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Configuración")
    
    if st.button("🔄 REINICIAR TURNO (Borrar Todo)"):
        st.session_state['datos'] = {}
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
            st.rerun()
        else:
            st.error("Debe quedar al menos 1 licor.")

# --- SELECCIÓN Y LÓGICA ---
licor_seleccionado = st.selectbox("Selecciona el Licor a cuadrar", list(st.session_state['licores'].keys()))
config = st.session_state['licores'][licor_seleccionado]

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
        d['ib'] = c1.number_input("Botellas", value=d['ib'], key=f"ib_{licor_seleccionado}")
        d['io'] = c2.number_input("OZ", value=d['io'], key=f"io_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>INGRESO</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['inb'] = c1.number_input("Botellas", value=d['inb'], key=f"inb_{licor_seleccionado}")
        d['ino'] = c2.number_input("OZ", value=d['ino'], key=f"ino_{licor_seleccionado}")

    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>SALIDA</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['sb'] = c1.number_input("Botellas", value=d['sb'], key=f"sb_{licor_seleccionado}")
        d['so'] = c2.number_input("OZ", value=d['so'], key=f"so_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>BOT ABIERTA PARA COCTEL</h4>", unsafe_allow_html=True)
        d['ba'] = st.number_input("Botellas a abrir", value=d['ba'], key=f"ba_{licor_seleccionado}")

with col_der:
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>VENTA</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['vb'] = c1.number_input("Botellas", value=d['vb'], key=f"vb_{licor_seleccionado}")
        d['vt'] = c2.number_input("Tragos", value=d['vt'], key=f"vt_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>CORTESÍA</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['cb'] = c1.number_input("Botellas", value=d['cb'], key=f"cb_{licor_seleccionado}")
        d['ct'] = c2.number_input("Tragos", value=d['ct'], key=f"ct_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>TICKETS</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        d['tb'] = c1.number_input("Botellas", value=d['tb'], key=f"tb_{licor_seleccionado}")
        d['tt'] = c2.number_input("Tragos", value=d['tt'], key=f"tt_{licor_seleccionado}")
        
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0px;'>PUERTA</h4>", unsafe_allow_html=True)
        d['pb'] = st.number_input("Botellas Cerradas", value=d['pb'], key=f"pb_{licor_seleccionado}")

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
# Usamos st.table para que sea una tabla fija sin índices numéricos extra
st.table(pd.DataFrame(resumen_data))
