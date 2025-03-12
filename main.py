import streamlit as st
import requests
import re

def convertir_link_gdrive(url):
    """
    Extrae el id del archivo desde la URL de Google Drive y retorna el link para descarga directa.
    """
    match = re.search(r'/d/([^/]+)', url)
    if match:
        file_id = match.group(1)
        nuevo_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return nuevo_url
    else:
        return url  # Retorna la URL original si no se encuentra el patrón

st.title("Envío de Datos a API")

# Entradas de usuario
link_original = st.text_input("Ingresa el link del archivo (Google Drive)")
medida_x = st.text_input("Ingresa la medida x")
medida_y = st.text_input("Ingresa la medida y")
nombre = st.text_input("Ingresa un nombre")

# Diccionario con los nombres y correos
correos = {
    "Karim Acuña": "kacuna@buhoms.com",
    "Mariana Hernández": "print@buhoms.com",
    "Mauricio Fernandez": "mfernandez@buhoms.com",
    "Pablo Faz": "pfaz@buhoms.com",
    "Susana Hernández": "shernandez@buhoms.com"
}

# Crear lista de nombres ordenados alfabéticamente
nombres_ordenados = sorted(correos.keys())

# Dropdown para seleccionar el nombre
nombre_seleccionado = st.selectbox("Selecciona el nombre", nombres_ordenados)

# Obtener el correo correspondiente al nombre seleccionado
correo_seleccionado = correos[nombre_seleccionado]

if st.button("Enviar"):
    # Convertir el link de Google Drive a link de descarga directa
    link_convertido = convertir_link_gdrive(link_original)
    
    # Preparar el payload para la API en formato multipart/form-data
    payload = {
        'file': (None, link_convertido),
        'medida_x': (None, medida_x),
        'medida_y': (None, medida_y),
        'nombre': (None, nombre),
        'email': (None, correo_seleccionado)
    }
    
    url_api = "http://189.192.20.132:51088/scripting/notify"
    
    try:
        # Enviar la solicitud POST usando 'files' para que se envíe como multipart/form-data
        response = requests.post(url_api, files=payload)
        
        st.write("**Código de estado:**", response.status_code)
        st.write("**Respuesta de la API:**")
        st.code(response.text)
        
        if response.status_code == 200:
            st.success("Datos enviados correctamente")
        else:
            st.error("Error al enviar los datos")
            
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
