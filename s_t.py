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

# CSS personalizado para dark mode
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
        
        /* Todos los textos en blanco */
        * {
            color: var(--text-color) !important;
        }
        
        body {
            background-color: var(--primary-bg);
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Contenedor principal */
        .stApp {
            background-color: var(--primary-bg);
            padding: 1rem;
        }
        
        /* Sidebar */
        .stSidebar {
            background-color: var(--secondary-bg) !important;
            border-right: 1px solid var(--border-color);
        }
        
        /* Botones de Bokeh */
        .bk-btn {
            background-color: var(--accent-color) !important;
            color: white !important;
            border: 3px !important;
            border-radius: 8px !important;
            font-size: 16px !important;
        }
        
        /* Select boxes */
        .stSelectbox select {
            background-color: var(--element-bg) !important;
            color: white !important;
            border: 1px solid var(--border-color) !important;
        }
        
        /* Checkbox */
        .stCheckbox label {
            color: white !important;
        }
        
        /* Imágenes */
        .stImage {
            border: 2px solid var(--border-color);
            border-radius: 8px;
        }
        
        /* Audio player */
        audio {
            filter: invert(1) hue-rotate(180deg);
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎤TRADUCTOR DE VOZ GPT🎤")
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

# Botón de grabación
stt_button = Button(label=" 🎤 Escuchar", width=300, height=50, css_classes=["bk-btn"])

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.success("🎙️ Texto reconocido:")
        st.code(result.get("GET_TEXT"), language="text")
    
    try:
        os.mkdir("temp")
    except:
        pass
    
    st.markdown("## Configuración de Traducción")
    translator = Translator()
    
    text = str(result.get("GET_TEXT"))
    
    col1, col2 = st.columns(2)
    with col1:
        in_lang = st.selectbox(
            "Lenguaje de Entrada",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
        )
    with col2:
        out_lang = st.selectbox(
            "Lenguaje de Salida",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
        )
    
    # Mapeo de idiomas
    lang_map = {
        "Inglés": "en",
        "Español": "es",
        "Bengali": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja"
    }
    
    input_language = lang_map[in_lang]
    output_language = lang_map[out_lang]
    
    english_accent = st.selectbox(
        "Acento de Pronunciación",
        ("Defecto", "Español", "Reino Unido", "Estados Unidos", "Canada", 
         "Australia", "Irlanda", "Sudáfrica"),
    )
    
    # Mapeo de acentos
    accent_map = {
        "Defecto": "com",
        "Español": "com.mx",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canada": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za"
    }
    
    tld = accent_map[english_accent]
    
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20].replace(" ", "_")
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    display_output_text = st.checkbox("Mostrar texto traducido")
    
    if st.button("🔊 Convertir a Audio", type="primary"):
        with st.spinner("Traduciendo y generando audio..."):
            try:
                result, output_text = text_to_speech(input_language, output_language, text, tld)
                audio_file = open(f"temp/{result}.mp3", "rb")
                audio_bytes = audio_file.read()
                
                st.markdown("## 🔊 Audio Traducido")
                st.audio(audio_bytes, format="audio/mp3")
                
                if display_output_text:
                    st.markdown("## 📝 Texto Traducido")
                    st.write(output_text)
                    
            except Exception as e:
                st.error(f"Error en la conversión: {str(e)}")
    
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)

# Pie de página
st.markdown("---")
st.caption("Traductor de Voz | Desarrollado con Streamlit")
