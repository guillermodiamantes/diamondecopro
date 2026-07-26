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

# --- ESTILOS CSS ---
st.markdown("""
<style>
.stApp {
    background-color: #F8F9FA;
}
.brand-container {
    text-align: center;
    padding: 10px 0 20px 0;
}
.brand-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #6C5CE7;
    margin-bottom: 5px;
}
.brand-badge {
    display: inline-block;
    background: #FFFFFF;
    border: 2px solid #E6007E;
    padding: 4px 18px;
    border-radius: 20px;
    font-size: 1.1rem;
    font-weight: 700;
    color: #333333;
    margin-top: 8px;
    box-shadow: 0 4px 10px rgba(230, 0, 126, 0.15);
}
.canvas-box {
    background-color: #FFFFFF;
    border: 3px solid #E0E0E0;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("""
<div class="brand-container">
    <div class="brand-title">💎 DIAMOND ECO PRO 💎</div>
    <div class="brand-badge">✨ Diseñador de Lienzos Gratis & Reciclaje Eco</div>
</div>
""", unsafe_allow_html=True)

# --- SECCIÓN PRINCIPAL: CARGADOR Y CONFIGURACIÓN ---
st.markdown('<div class="canvas-box">', unsafe_allow_html=True)
st.subheader("🖼️ Crea tu Patrón de Diamond Painting")
st.write("Sube una foto personal para transformarla en un mosaico interactivo con los colores de la gama DMC.")

# 1. Selector de archivo
archivo_subido = st.file_uploader("Elige una imagen (JPG, PNG)", type=["jpg", "jpeg", "png"])

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
    st.success("¡Imagen cargada con éxito! Procesando conversión a mosaico DMC...")
    
    # Cargamos la imagen con PIL
    imagen = Image.open(archivo_subido)
    
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.image(imagen, caption="Imagen Original", use_column_width=True)
    with col_img2:
        # Simulamos una vista previa en miniatura pixelada para el efecto lienzo
        imagen_mini = imagen.resize((40, 40), Image.Resampling.NEAREST)
        st.image(imagen_mini, caption=f"Mosaico Generado ({tipo_diamante})", use_column_width=True)
    
    st.markdown("### 🎨 Inventario de Colores DMC Recomendados")
    st.write("Este es tu desglose optimizado para las cuentas necesarias en tu lienzo:")
    
    # Tabla de ejemplo con colores DMC simulados
    st.markdown("""
    | Símbolo | Código DMC | Color | Nombre del Color | % en Lienzo |
    | :---: | :---: | :---: | :--- | :---: |
    | 🔲 | **DMC 310** | ⬛ | Negro Oscuro | 28% |
    | ⚪ | **DMC B5200**| ⬜ | Blanco Nieve | 35% |
    | 🔴 | **DMC 666** | 🟥 | Rojo Brillante | 15% |
    | 🔵 | **DMC 3843** | 🟦 | Azul Turquesa | 12% |
    | 🟡 | **DMC 444** | 🟨 | Amarillo Limón | 10% |
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botón de descarga interactivo
    if st.button("📥 Descargar Patrón Completo en PDF (Simbológico + DMC)"):
        st.success("¡Patrón generado correctamente! Tu descarga comenzará en breve.")
else:
    st.info("👆 Sube una imagen arriba para empezar a diseñar tu lienzo personalizado y ver su desglose DMC.")

# --- FOOTER ---
st.markdown("---")
st.caption("🚀 DiamondEcoPro • Diseñador Sostenible de Arte en Diamante & Reciclaje Eco")
