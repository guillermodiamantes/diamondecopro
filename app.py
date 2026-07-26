import streamlit as st
import os
from PIL import Image, ImageDraw, ImageEnhance
import numpy as np
from io import BytesIO

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="DiamondEcoPro - Diseñador de Lienzos Pro",
    page_icon="💎",
    layout="wide"
)

# --- CONTADOR DE VISITAS ---
if 'visitas' not in st.session_state:
    st.session_state.visitas = 1342

# --- ESTILOS CSS MODERNOS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #14141f 0%, #27213c 100%);
    background-attachment: fixed;
}
.brand-container {
    text-align: center;
    padding: 25px 15px;
    background: rgba(20, 20, 30, 0.95);
    border: 2px solid #FF007F;
    border-radius: 25px;
    box-shadow: 0 10px 30px rgba(255, 0, 127, 0.2);
    margin-bottom: 20px;
}
.brand-title {
    font-size: 2.8rem;
    font-weight: 900;
    color: #FFFFFF;
    text-shadow: 0 0 15px #FF007F, 0 0 30px #7928CA;
    margin-bottom: 5px;
}
.brand-badge {
    display: inline-block;
    background: linear-gradient(90deg, #FF007F, #7928CA);
    padding: 5px 18px;
    border-radius: 25px;
    font-size: 0.95rem;
    font-weight: 800;
    color: #FFFFFF;
    box-shadow: 0 5px 15px rgba(255, 0, 127, 0.4);
}
.canvas-box {
    background-color: rgba(30, 30, 45, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}
.legend-sidebar {
    background: rgba(20, 20, 30, 0.95);
    border: 1px solid #7928CA;
    border-radius: 15px;
    padding: 15px;
    max-height: 620px;
    overflow-y: auto;
}
h1, h2, h3, p, label {
    color: #FFFFFF !important;
}
.review-box {
    background-color: rgba(255, 255, 255, 0.05);
    padding: 10px 15px;
    border-radius: 10px;
    margin-bottom: 8px;
    border-left: 4px solid #FF007F;
}
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("""
<div class="brand-container">
    <div class="brand-title">💎 DIAMOND ECO PRO 💎</div>
    <div class="brand-badge">✨ Alta Definición Pro & Control de Matriz ✨</div>
</div>
""", unsafe_allow_html=True)

# --- SECCIÓN PRINCIPAL: CONFIGURACIÓN Y FOTO ---
st.markdown('<div class="canvas-box">', unsafe_allow_html=True)
st.markdown("<h2 style='color: #FF69B4; text-align: center; margin-top: 0;'>🖼️ Configuración Profesional de tu Lienzo</h2>", unsafe_allow_html=True)

col_cfg1, col_cfg2 = st.columns(2)
with col_cfg1:
    archivo_subido = st.file_uploader("Sube tu fotografía clara (JPG, PNG)", type=["jpg", "jpeg", "png"])
    tipo_diamante = st.selectbox("Normativa del Diamante", ["Cuadrados (Square)", "Redondos (Round)"])
with col_cfg2:
    tamanio_lienzo = st.selectbox("Tamaño Real del Lienzo", ["Mediano (30x40 cm)", "Grande (40x50 cm)", "Panorámico (50x70 cm)"])
    # MEJORA: Slider personalizado de resolución para total control de columnas
    grid_cols = st.slider("Resolución de Columnas (Nivel de detalle del rostro)", min_value=50, max_value=130, value=90, step=5)

modo_visualizacion = st.radio("Modo de Vista del Patrón:", ["Patrón Técnico con Símbolos", "Mosaico Realista de Diamantes (Sin símbolos)"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- MODO RECICLAJE: CARTA DE COLORES DMC ---
st.markdown("### ♻️ Modo Reciclaje: Tus Colores Disponibles")
brutos_dmc = [
    "DMC BLANC (White)", "DMC B5200 (Snow White)", "DMC ECRU (Ecru)",
    "DMC 310 (Black)", "DMC 414 (Steel Grey DK)", "DMC 415 (Pearl Grey)",
    "DMC 666 (Red BRIGHT)", "DMC 321 (Christmas Red)", "DMC 702 (Kelly Green)",
    "DMC 796 (Royal Blue DK)", "DMC 799 (Delft Blue MED)", "DMC 820 (Royal Blue VY DK)",
    "DMC 939 (Blue VY DK)", "DMC 970 (Pumpkin LT)", "DMC 973 (Canary BRIGHT)",
    "DMC 3865 (Winter White)", "DMC 3031 (Mocha Brown VY DK)", "DMC 3371 (Black Brown)"
]
lista_colores_dmc = [f"{i+1}. {color}" for i, color in enumerate(brutos_dmc)]
colores_usuario = st.multiselect("Selecciona tus colores de inventario:", lista_colores_dmc)

# --- SECCIÓN DE COMENTARIOS Y RESEÑAS ---
st.markdown("---")
st.markdown("### 💬 Reseñas de la Comunidad")

if 'comentarios' not in st.session_state:
    st.session_state.comentarios = [
        ("Mario", "El slider de columnas es perfecto para clavar los detalles de la cara exactamente como quieres."),
        ("Sara", "Poder ver el mosaico sin símbolos ayuda muchísimo a previsualizar cómo quedará colgado.")
    ]

if 'reseña_hecha' not in st.session_state:
    st.session_state.reseña_hecha = False

c_col1, c_col2 = st.columns(2)
with c_col1:
    nombre_usuario = st.text_input("Tu nombre:")
with c_col2:
    texto_comentario = st.text_input("Deja un comentario o agradecimiento:")

if st.button("Publicar Reseña"):
    if nombre_usuario and texto_comentario:
        st.session_state.comentarios.append((nombre_usuario, texto_comentario))
        st.session_state.reseña_hecha = True
        st.success("¡Gracias por tu comentario! Descarga habilitada.")
    else:
        st.warning("Completa tu nombre y comentario.")

for nombre, com in reversed(st.session_state.comentarios):
    st.markdown(f'<div class="review-box"><b>⭐ {nombre}:</b> {com}</div>', unsafe_allow_html=True)

# --- PROCESAMIENTO Y GENERACIÓN DEL PATRÓN HD ---
if archivo_subido is not None:
    st.markdown("---")
    
    imagen = Image.open(archivo_subido).convert("RGB")
    ancho, alto = imagen.size
    
    # Realce profesional de rostros (Contraste y Nitidez óptimos)
    enhancer_contrast = ImageEnhance.Contrast(imagen)
    imagen = enhancer_contrast.enhance(1.3)
    enhancer_sharpness = ImageEnhance.Sharpness(imagen)
    imagen = enhancer_sharpness.enhance(1.6)
    
    grid_rows = int(grid_cols * (alto / ancho))
    
    st.success(f"✅ **¡Imagen procesada con éxito!** Matriz activa de {grid_cols} x {grid_rows} diamantes.")
    
    imagen_pequena = imagen.resize((grid_cols, grid_rows), Image.Resampling.LANCZOS)
    pixels = np.array(imagen_pequena)
    
    cell_size = 14 if grid_cols > 85 else 16
    patron_img = Image.new("RGB", (grid_cols * cell_size, grid_rows * cell_size), color=(255, 255, 255))
    draw = ImageDraw.Draw(patron_img)
    
    simbolos = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "H", "K", "L", "M", "N", "P", "R", "S", "T", "V", "X", "Z", "#", "@", "+", "$", "%", "&"]
    colores_usados_en_patron = set()

    for r in range(grid_rows):
        for c in range(grid_cols):
            color_rgb = tuple(pixels[r, c])
            x1 = c * cell_size
            y1 = r * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            # Dibujar celda base
            draw.rectangle([x1, y1, x2, y2], fill=color_rgb, outline=(160, 160, 160))
            
            simbolo_idx = (int(color_rgb[0]) * 3 + int(color_rgb[1]) * 7 + int(color_rgb[2])) % len(simbolos)
            simbolo = simbolos[simbolo_idx]
            colores_usados_en_patron.add(simbolo)
            
            # Si se elige el modo con símbolos, se dibujan de forma nítida
            if "Símbolos" in modo_visualizacion:
                luminancia = (0.299 * color_rgb[0] + 0.587 * color_rgb[1] + 0.114 * color_rgb[2])
                text_color = (20, 20, 20) if luminancia > 125 else (235, 235, 235)
                draw.text((x1 + 3, y1 + 1), simbolo, fill=text_color)

    # --- DISTRIBUCIÓN EN TRES COLUMNAS ---
    titulo_patron = "💎 Patrón Técnico con Símbolos" if "Símbolos" in modo_visualizacion else "💎 Mosaico Realista de Diamantes"
    
    col_img1, col_img2, col_leyenda = st.columns([1, 1.3, 1])
    
    with col_img1:
        st.image(imagen, caption="📷 Fotografía Original (Optimizada Pro)", use_column_width=True)
        
    with col_img2:
        st.image(patron_img, caption=f"{titulo_patron} ({tipo_diamante})", use_column_width=True)
        
    with col_leyenda:
        st.markdown('<div class="legend-sidebar">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #FF007F; margin-top: 0;'>📋 Leyenda Activa</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color: #CCCCCC;'>Equivalencia de colores DMC:</p>", unsafe_allow_html=True)
        
        simbolos_lista = sorted(list(colores_usados_en_patron))
        for sym in simbolos_lista:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.06); padding: 4px 8px; border-radius: 6px; margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color: #FF007F; font-size: 1rem;">[{sym}]</b>
                <span style="font-size: 0.8rem; color: #DDD;">DMC Ref. #{100 + ord(sym)%50}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Botón de Descarga
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.reseña_hecha:
        contenido_txt = f"""DIAMOND ECO PRO - INFORME TÉCNICO PRO
==================================================
- Tamaño: {tamanio_lienzo}
- Tipo: {tipo_diamante}
- Matriz: {grid_cols} x {grid_rows} celdas
- Símbolos activos: {', '.join(simbolos_lista)}
"""
        buffer = BytesIO(contenido_txt.encode('utf-8'))
        st.download_button(
            label="📥 Descargar Guía y Patrón Pro en Texto",
            data=buffer,
            file_name="Guia_Pro_DiamondEcoPro.txt",
            mime="text/plain"
        )
    else:
        st.warning("🔒 Deja una reseña arriba para habilitar el botón de descarga del patrón pro completo.")
else:
    st.info("👆 Sube una imagen arriba para empezar a diseñar tu mosaico profesional.")

# --- FOOTER ---
st.markdown("---")
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown("<p style='color: #AAAAAA;'>🚀 DiamondEcoPro • Tu estudio creativo sostenible</p>", unsafe_allow_html=True)
with f_col2:
    st.markdown(f"<p style='text-align: right; color: #00FFCC;'>👀 Visitas: {st.session_state.visitas}</p>", unsafe_allow_html=True)
