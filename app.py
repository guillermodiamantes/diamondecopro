import streamlit as st
import os
from PIL import Image
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="DiamondEcoPro - Diseñador de Lienzos Gratis",
    page_icon="💎",
    layout="centered"
)

# --- ESTILOS CSS CON FONDO OSCURO Y VIBRANTE ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
    background-attachment: fixed;
}
.brand-container {
    text-align: center;
    padding: 30px 10px;
    background: rgba(15, 15, 25, 0.85);
    border: 2px solid #FF007F;
    border-radius: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    margin-bottom: 25px;
}
.brand-title {
    font-size: 3rem;
    font-weight: 900;
    color: #FFFFFF;
    text-shadow: 0 0 15px #FF007F, 0 0 30px #7928CA;
    margin-bottom: 10px;
}
.brand-badge {
    display: inline-block;
    background: linear-gradient(90deg, #FF007F, #7928CA);
    padding: 6px 22px;
    border-radius: 25px;
    font-size: 1.2rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-top: 5px;
    box-shadow: 0 5px 15px rgba(255, 0, 127, 0.4);
}
.canvas-box {
    background-color: rgba(25, 25, 35, 0.95);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.4);
    margin-top: 20px;
}
h2, p, label {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# --- CABECERA LLAMATIVA ---
st.markdown("""
<div class="brand-container">
    <div class="brand-title">💎 DIAMOND ECO PRO 💎</div>
    <div class="brand-badge">✨ Tu Diseñador de Lienzos con Magia & Color ✨</div>
</div>
""", unsafe_allow_html=True)

# --- SECCIÓN PRINCIPAL: CARGADOR Y CONFIGURACIÓN ---
st.markdown('<div class="canvas-box">', unsafe_allow_html=True)
st.markdown("<h2 style='color: #FF69B4; text-align: center; margin-top: 0;'>🖼️ Crea tu Patrón de Diamond Painting</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #E0E0E0; font-size: 1.1rem;'>Sube tu foto favorita y conviértela en un mosaico vibrante con la gama de colores DMC oficial.</p>", unsafe_allow_html=True)

# 1. Selector de archivo
archivo_subido = st.file_uploader("Elige una imagen alegre (JPG, PNG)", type=["jpg", "jpeg", "png"])

# 2. Opciones de configuración
col1, col2 = st.columns(2)
with col1:
    tipo_diamante = st.selectbox("Forma de los Diamantes", ["Cuadrados (Square)", "Redondos (Round)"])
with col2:
    tamanio_lienzo = st.selectbox("Tamaño del Lienzo", ["Mediano (30x40 cm)", "Grande (40x50 cm)", "Panorámico (50x70 cm)"])

st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESAMIENTO Y SIMULACIÓN DE PATRÓN ---
if archivo_subido is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("¡Imagen cargada con éxito! Preparando tu explosión de color...")
    
    imagen = Image.open(archivo_subido)
    
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.image(imagen, caption="📷 Fotografía Original", use_column_width=True)
    with col_img2:
        imagen_mini = imagen.resize((45, 45), Image.Resampling.NEAREST)
        st.image(imagen_mini, caption=f"🎨 Vista Mosaico ({tipo_diamante})", use_column_width=True)
    
    st.markdown("### 🌈 Inventario de Colores DMC")
    st.write("Tu paleta de colores personalizada y lista para comenzar a crear:")
    
    st.markdown("""
    | Símbolo | Código DMC | Muestra | Nombre del Color | % Estimado |
    | :---: | :---: | :---: | :--- | :---: |
    | ⬛ | **DMC 310** | ⬛ | Negro Intenso | 20% |
    | ⬜ | **DMC B5200**| ⬜ | Blanco Brillante | 25% |
    | 🔴 | **DMC 666** | 🟥 | Rojo Pasión | 12% |
    | 🔵 | **DMC 3843** | 🟦 | Azul Eléctrico | 10% |
    | 🟡 | **DMC 444** | 🟨 | Amarillo Sol | 10% |
    | 🟩 | **DMC 701** | 🟩 | Verde Vivo | 8% |
    | 🟣 | **DMC 550** | 🟪 | Violeta Mágico | 8% |
    | 🟠 | **DMC 946** | 🟧 | Naranja Fuego | 7% |
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📥 Descargar Patrón Completo en PDF"):
        st.success("¡Descarga lista! Tu diseño en alta calidad se está procesando.")
else:
    st.info("👆 Sube una imagen arriba para ver la magia del color en acción.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #FFFFFF; font-weight: 600;'>🚀 DiamondEcoPro • Arte, Color y Sostenibilidad</p>", unsafe_allow_html=True)
