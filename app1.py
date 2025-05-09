# -*- coding: utf-8 -*-
"""
Created on Fri May  9 16:29:06 2025

@author: jahop
"""

import streamlit as st
from datetime import datetime, time
import pandas as pd
import base64

# Configuración de la página
st.set_page_config(
    page_title="Sistema Front Desk BBVA", 
    layout="wide",
    page_icon="🏦"
)

# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)




# Título principal
st.title('📋 Sistema de Gestión para Front Desk - BBVA AutoMarket')

# Inicializar session_state para cada DataFrame si no existen
if 'registros_visitantes' not in st.session_state:
    st.session_state.registros_visitantes = pd.DataFrame(columns=["Nombre", "Documento", "Motivo", "Entrada", "Salida"])
    
if 'registros_citas' not in st.session_state:
    st.session_state.registros_citas = pd.DataFrame(columns=["Cliente", "Fecha", "Hora", "Motivo"])
    
if 'registros_documentos' not in st.session_state:
    st.session_state.registros_documentos = pd.DataFrame(columns=["Tipo", "Estado", "Observaciones", "Fecha"])
    
if 'registros_llamadas' not in st.session_state:
    st.session_state.registros_llamadas = pd.DataFrame(columns=["Teléfono", "Motivo", "Atendido por", "Detalles", "Fecha"])

# Función para descargar DataFrames como CSV
def get_table_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Descargar archivo CSV</a>'
    return href

# Sidebar - Sección de usuario
st.sidebar.markdown("## 👤 Javier horacio Pérez Ricárdez")
st.sidebar.markdown("*Front Desk Manager*")
st.sidebar.markdown("---")

# Sidebar - Menú de opciones
st.sidebar.markdown("## 🚀 Navegación")
opcion = st.sidebar.selectbox('Seleccione una función:', 
                            ['Registro de Visitantes', 
                             'Gestión de Citas', 
                             'Control Documental',
                             'Panel de Llamadas'])

# Sidebar - Sección de Ayuda
st.sidebar.markdown("---")
st.sidebar.markdown("## ❓ Ayuda")

with st.sidebar.expander("Cómo usar esta aplicación"):
    st.markdown("""
    **Guía rápida:**
    
    1. **Seleccione una función** en el menú desplegable
    2. **Complete el formulario** correspondiente
    3. **Los datos se guardan automáticamente** en la sesión actual
    4. **Exporte a CSV** cuando necesite guardar los registros
    
    **Funciones disponibles:**
    - 👥 Registro de visitantes (entradas/salidas)
    - 📅 Gestión de citas con clientes
    - 📄 Control de documentos recibidos
    - 📞 Registro de llamadas entrantes
    """)

with st.sidebar.expander("Soporte técnico"):
    st.markdown("""
    **Para asistencia técnica:**
    
    📧 Email: soporte@bbva.com  
    ☎ Teléfono:  +55 5226 2663  
    🏢 Oficina: Torre BBVA, CDMX
    
    **Horario de soporte:**
    Lunes a Viernes: 8:00 - 20:00
    """)

# Sidebar - Información del sistema
st.sidebar.markdown("---")
st.sidebar.markdown("""
**ℹ Información del sistema**  
Versión: 1.1  
Última actualización: 09/05/2025  
Desarrollado por: **Javier Horacio Pérez Ricárdez**  
""")

# Contenido principal según la opción seleccionada
if opcion == 'Registro de Visitantes':
    st.header('👥 Registro de Visitantes')
    
    with st.form("registro_form"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo*", help="Nombre y apellidos del visitante")
            documento = st.text_input("Número de documento*")
        with col2:
            motivo = st.selectbox("Motivo de la visita*", 
                                ["Compra de vehículo", "Consulta de crédito", "Entrega documentación", "Otro"])
            hora_entrada = st.time_input("Hora de entrada*", datetime.now().time())
        
        submit_button = st.form_submit_button("Registrar Visitante")
        
        if submit_button:
            if nombre and documento:  # Validación básica
                nuevo_registro = pd.DataFrame([[nombre, documento, motivo, hora_entrada.strftime("%H:%M"), None]],
                                             columns=["Nombre", "Documento", "Motivo", "Entrada", "Salida"])
                st.session_state.registros_visitantes = pd.concat([st.session_state.registros_visitantes, nuevo_registro])
                st.success(f"✅ Visitante {nombre} registrado correctamente a las {hora_entrada.strftime('%H:%M')}")
            else:
                st.error("Por favor complete los campos obligatorios (*)")
    
    # Sección para registrar salida
    st.subheader("Registrar Salida")
    if not st.session_state.registros_visitantes.empty:
        visitante_salida = st.selectbox("Seleccione visitante para registrar salida", 
                                       st.session_state.registros_visitantes["Nombre"])
        if st.button("Registrar Salida"):
            idx = st.session_state.registros_visitantes[st.session_state.registros_visitantes["Nombre"] == visitante_salida].index[0]
            st.session_state.registros_visitantes.at[idx, "Salida"] = datetime.now().strftime("%H:%M")
            st.success(f"Salida registrada para {visitante_salida}")
    
    st.subheader("📊 Registros del día")
    st.dataframe(st.session_state.registros_visitantes)
    
    if not st.session_state.registros_visitantes.empty:
        st.markdown(get_table_download_link(st.session_state.registros_visitantes, "registro_visitantes.csv"), unsafe_allow_html=True)

elif opcion == 'Gestión de Citas':
    st.header('📅 Gestión de Citas')
    
    with st.form("cita_form"):
        col1, col2 = st.columns(2)
        with col1:
            cliente = st.text_input("Nombre del cliente*")
            fecha = st.date_input("Fecha de la cita*", datetime.now())
        with col2:
            hora = st.time_input("Hora de la cita*", time(9, 0))
            motivo = st.text_area("Motivo de la cita*")
        
        submit_button = st.form_submit_button("Agendar Cita")
        
        if submit_button:
            if cliente and motivo:  # Validación básica
                nueva_cita = pd.DataFrame([[cliente, fecha.strftime("%Y-%m-%d"), hora.strftime("%H:%M"), motivo]],
                                         columns=["Cliente", "Fecha", "Hora", "Motivo"])
                st.session_state.registros_citas = pd.concat([st.session_state.registros_citas, nueva_cita])
                st.success(f"✅ Cita agendada para {cliente} el {fecha} a las {hora.strftime('%H:%M')}")
            else:
                st.error("Por favor complete los campos obligatorios (*)")
    
    st.subheader("📅 Citas Agendadas")
    st.dataframe(st.session_state.registros_citas)
    
    if not st.session_state.registros_citas.empty:
        st.markdown(get_table_download_link(st.session_state.registros_citas, "registro_citas.csv"), unsafe_allow_html=True)

elif opcion == 'Control Documental':
    st.header('📄 Control Documental')
    
    with st.form("documento_form"):
        col1, col2 = st.columns(2)
        with col1:
            tipo_doc = st.selectbox("Tipo de documento*", 
                                  ["Contrato de compraventa", "Solicitud de crédito", "Identificación", "Otro"])
            estado = st.radio("Estado del documento*", ["Recibido", "Digitalizado", "Verificado", "Archivado"])
        with col2:
            observaciones = st.text_area("Observaciones")
        
        submit_button = st.form_submit_button("Registrar Documento")
        
        if submit_button:
            nuevo_documento = pd.DataFrame([[tipo_doc, estado, observaciones, datetime.now().strftime("%Y-%m-%d %H:%M")]],
                                         columns=["Tipo", "Estado", "Observaciones", "Fecha"])
            st.session_state.registros_documentos = pd.concat([st.session_state.registros_documentos, nuevo_documento])
            st.success("✅ Documento registrado en el sistema")
    
    st.subheader("📋 Documentos Registrados")
    st.dataframe(st.session_state.registros_documentos)
    
    if not st.session_state.registros_documentos.empty:
        st.markdown(get_table_download_link(st.session_state.registros_documentos, "registro_documentos.csv"), unsafe_allow_html=True)

elif opcion == 'Panel de Llamadas':
    st.header('📞 Panel de Llamadas')
    
    with st.form("llamada_form"):
        col1, col2 = st.columns(2)
        with col1:
            telefono = st.text_input("Número telefónico*")
            motivo = st.selectbox("Motivo de la llamada*", 
                                ["Consulta general", "Seguimiento de crédito", "Agendar cita", "Reclamo"])
        with col2:
            atendido_por = st.text_input("Atendido por*", "Juan Pérez")
            detalles = st.text_area("Detalles de la llamada*")
        
        submit_button = st.form_submit_button("Registrar Llamada")
        
        if submit_button:
            if telefono and detalles:  # Validación básica
                nueva_llamada = pd.DataFrame([[telefono, motivo, atendido_por, detalles, datetime.now().strftime("%Y-%m-%d %H:%M")]],
                                           columns=["Teléfono", "Motivo", "Atendido por", "Detalles", "Fecha"])
                st.session_state.registros_llamadas = pd.concat([st.session_state.registros_llamadas, nueva_llamada])
                st.success("✅ Llamada registrada correctamente")
            else:
                st.error("Por favor complete los campos obligatorios (*)")
    
    st.subheader("📞 Llamadas Registradas")
    st.dataframe(st.session_state.registros_llamadas)
    
    if not st.session_state.registros_llamadas.empty:
        st.markdown(get_table_download_link(st.session_state.registros_llamadas, "registro_llamadas.csv"), unsafe_allow_html=True)

# Botón para resetear datos (solo para desarrollo)
if st.sidebar.button("⚠️ Resetear todos los datos"):
    st.session_state.registros_visitantes = pd.DataFrame(columns=["Nombre", "Documento", "Motivo", "Entrada", "Salida"])
    st.session_state.registros_citas = pd.DataFrame(columns=["Cliente", "Fecha", "Hora", "Motivo"])
    st.session_state.registros_documentos = pd.DataFrame(columns=["Tipo", "Estado", "Observaciones", "Fecha"])
    st.session_state.registros_llamadas = pd.DataFrame(columns=["Teléfono", "Motivo", "Atendido por", "Detalles", "Fecha"])
    st.sidebar.success("Todos los datos han sido reseteados")
