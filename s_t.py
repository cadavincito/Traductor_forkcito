import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
from gtts import gTTS
from googletrans import Translator

# Configuración de la página con tema oscuro
st.set_page_config(
    page_title="Traductor de Voz",
    page_icon="🎤",
    layout="centered"
)

# CSS personalizado para dark mode - VERSIÓN FINAL
st.markdown("""
    <style>
        /* Tema oscuro principal */
        :root {
            --primary-bg: #2D2D2D;
            --secondary-bg: #252525;
            --element-bg: #333333;
            --border-color: #444444;
            --text-color: #FFFFFF;
            --accent-color: #4F8BF9;
        }
        
        /* Reset completo para contenedores Bokeh */
        div[data-testid="stBokehChart"] > div > div,
        div[data-testid="stBokehChart"] > div > div > div,
        .bk-root .bk,
        .bk-canvas-wrapper,
        .bk-canvas,
        .bk-widget {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Eliminar cualquier fondo blanco residual */
        div[data-testid="stBokehChart"] {
            background-color: transparent !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Botón de Bokeh con estilo mejorado */
        .bk-btn {
            background-color: var(--accent-color) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            padding: 12px 24px !important;
            width: 300px !important;
            height: 50px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
            margin: 10px 0 !important;
        }
        
        .bk-btn:hover {
            opacity: 0.9 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        }
        
        /* Estilos generales de la aplicación */
        * {
            color: var(--text-color) !important;
        }
        
        body {
            background-color: var(--primary-bg);
            font-family: 'Segoe UI', sans-serif;
        }
        
        .stApp {
            background-color: var(--primary-bg);
            padding: 1rem;
        }
        
        /* ... (otros estilos se mantienen igual) ... */
    </style>
""", unsafe_allow_html=True)

# Resto del código se mantiene igual...
st.title("🎤 TRADUCTOR DE VOZ GPT")
st.subheader("Escucho lo que quieres traducir")

# Mostrar imagen
image = Image.open('img.jpg')
st.image(image, width=300)

with st.sidebar:
    st.subheader("Configuración")
    st.markdown("""
    1. Presiona el botón 🎤
    2. Habla cuando veas la señal
    3. Selecciona los idiomas
    4. Presiona "Convertir"
    """)

st.markdown("### Toca el botón y habla lo que quieres traducir")
