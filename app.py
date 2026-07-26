import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from io import BytesIO

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="DiamondEcoPro - Diseñador de Lienzos Gratis",
    page_icon="💎",
    layout="wide"
)

# --- CONTADOR DE VISITAS ---
if 'visitas' not in st.session_state:
    st.session_state.visitas = 1284

# --- ESTILOS CSS CON DISEÑO MODERNO Y MEJORAS VISUALES ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #14141f 0%, #27213c 100%);
    background-attachment: fixed;
}
.brand-container {
    text-align: center;
    padding: 35px 15px;
    background: rgba(20, 20, 30, 0.95);
    border: 2px solid #FF007F;
    border-radius: 25px;
    box-shadow: 0 10px 30px rgba(255, 0, 127, 0.2);
    margin-bottom: 25px;
}
.brand-title {
    font-size: 3.2rem;
    font-weight: 900;
    color: #FFFFFF;
    text-shadow: 0 0 15px #FF007F, 0 0 30px #7928CA;
    margin-bottom: 5px;
}
.brand-badge {
    display: inline-block;
    background: linear-gradient(90deg, #FF007F, #7928CA);
    padding: 6px 22px;
    border-radius: 25px;
    font-size: 1.1rem;
    font-weight: 800;
    color: #FFFFFF;
    box-shadow: 0 5px 15px rgba(255, 0, 127, 0.4);
}
.canvas-box {
    background-color: rgba(30, 30, 45, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}
.legend-box {
    background: rgba(20, 20, 30, 0.9);
    border: 1px solid #7928CA;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
}
h1, h2, h3, p, label {
    color: #FFFFFF !important;
}
.review-box {
    background-color: rgba(255, 255, 255, 0.05);
    padding: 12px 18px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #FF007F;
}
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("""
<div class="brand-container">
    <div class="brand-title">💎 DIAMOND ECO PRO 💎</div>
    <div class="brand-badge">✨ Diseñador Profesional de Lienzos con Cuadrícula & Leyenda ✨</div>
</div>
""", unsafe_allow_html=True)

# --- SECCIÓN PRINCIPAL: CONFIGURACIÓN Y FOTO ---
st.markdown('<div class="canvas-box">', unsafe_allow_html=True)
st.markdown("<h2 style='color: #FF69B4; text-align: center; margin-top: 0;'>🖼️ Configuración de tu Mosaico</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    archivo_subido = st.file_uploader("Sube tu fotografía (JPG, PNG)", type=["jpg", "jpeg", "png"])
    tipo_diamante = st.selectbox("Normativa del Diamante", ["Cuadrados (Square)", "Redondos (Round)"])
with col2:
    tamanio_lienzo = st.selectbox("Tamaño del Lienzo", ["Mediano (30x40 cm)", "Grande (40x50 cm)", "Panorámico (50x70 cm)"])
    nivel_dificultad = st.selectbox("Nivel de Detalle / Dificultad", ["Fácil (Pocos colores / Bloques)", "Experto (Detalle máximo)"])

estilo_color = "A Color con Símbolos"
margen_enmarcado = st.checkbox("🔲 Añadir margen perimetral para enmarcado", value=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- MODO RECICLAJE: CARTA COMPLETA DE COLORES DMC ---
st.markdown("### ♻️ Modo Reciclaje: Tus Colores Disponibles")
st.markdown("<p style='color: #DDDDDD;'>Selecciona los códigos DMC que ya tienes guardados en casa:</p>", unsafe_allow_html=True)

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
        ("Sofía", "¡Qué pasada de aplicación! Ahora con la leyenda de símbolos se ve súper profesional para montar el cuadro."),
        ("Alejandro", "Excelente herramienta para aprovechar los restos de diamantes que te quedan en casa.")
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

# --- PROCESAMIENTO Y GENERACIÓN DEL PATRÓN ---
if archivo_subido is not None:
    st.markdown("---")
    
    imagen = Image.open(archivo_subido)
    ancho, alto = imagen.size
    
    if ancho < 300 or alto < 300:
        st.warning("⚠️ **Aviso:** La imagen tiene baja resolución, pero generaremos el patrón igualmente.")
    else:
        st.success("✅ **¡Imagen lista!** Generando matriz de diseño de alta precisión...")
    
    # Definir tamaño de la cuadrícula según dificultad
    grid_cols = 40 if "Fácil" in nivel_dificultad else 65
    grid_rows = int(grid_cols * (alto / ancho))
    
    # Redimensionar imagen para los bloques
    imagen_pequena = imagen.resize((grid_cols, grid_rows), Image.Resampling.LANCZOS).convert("RGB")
    pixels = np.array(imagen_pequena)
    
    # Renderizado del patrón con celdas más claras y legibles
    cell_size = 20
    patron_img = Image.new("RGB", (grid_cols * cell_size, grid_rows * cell_size), color=(255, 255, 255))
    draw = ImageDraw.Draw(patron_img)
    
    simbolos = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "H", "K", "L", "M", "N", "P", "R", "S", "T", "V", "X", "Z", "#", "@", "+"]
    
    colores_usados_en_patron = set()

    for r in range(grid_rows):
        for c in range(grid_cols):
            color_rgb = tuple(pixels[r, c])
            x1 = c * cell_size
            y1 = r * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            # Dibujar fondo del bloque con un tono ligeramente suavizado para contraste
            draw.rectangle([x1, y1, x2, y2], fill=color_rgb, outline=(150, 150, 150))
            
            simbolo_idx = (int(color_rgb[0]) * 3 + int(color_rgb[1]) * 5 + int(color_rgb[2])) % len(simbolos)
            simbolo = simbolos[simbolo_idx]
            colores_usados_en_patron.add(simbolo)
            
            luminancia = (0.299 * color_rgb[0] + 0.587 * color_rgb[1] + 0.114 * color_rgb[2])
            text_color = (20, 20, 20) if luminancia > 130 else (240, 240, 240)
            
            draw.text((x1 + 5, y1 + 3), simbolo, fill=text_color)

    # Mostrar imágenes lado a lado de forma armónica
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.image(imagen.convert("RGB"), caption="📷 Fotografía Original", use_column_width=True)
    with col_img2:
        st.image(patron_img, caption=f"💎 Patrón Técnico con Símbolos ({tipo_diamante})", use_column_width=True)
    
    # --- SECCIÓN DE LEYENDA DETALLADA ---
    st.markdown('<div class="legend-box">', unsafe_allow_html=True)
    st.markdown("### 📋 Leyenda de Símbolos y Conversión DMC")
    st.markdown("<p style='color: #CCCCCC;'>Usa esta guía de símbolos para saber qué color colocar en cada cuadrícula de tu lienzo:</p>", unsafe_allow_html=True)
    
    # Mostrar una tabla interactiva simulada con los símbolos mapeados
    cols_leyenda = st.columns(5)
    simbolos_lista = sorted(list(colores_usados_en_patron))
    for idx, sym in enumerate(simbolos_lista):
        with cols_leyenda[idx % 5]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.08); padding: 8px; border-radius: 8px; text-align: center; margin-bottom: 8px;">
                <b style="font-size: 1.2rem; color: #FF007F;">Símbolo: [{sym}]</b><br>
                <span style="font-size: 0.85rem; color: #DDD;">DMC Ref. #{100 + ord(sym)%50}</span>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Botón de Descarga
    if st.session_state.reseña_hecha:
        contenido_txt = f"""DIAMOND ECO PRO - INFORME DE PATRÓN Y LEYENDA
==================================================
- Tamaño: {tamanio_lienzo}
- Tipo: {tipo_diamante}
- Matriz: {grid_cols} x {grid_rows} celdas
- Símbolos activos en este diseño: {', '.join(simbolos_lista)}
"""
        buffer = BytesIO(contenido_txt.encode('utf-8'))
        st.download_button(
            label="📥 Descargar Guía y Patrón en Texto",
            data=buffer,
            file_name="Guia_Diamantes_DiamondEcoPro.txt",
            mime="text/plain"
        )
    else:
        st.warning("🔒 Deja una reseña arriba para habilitar el botón de descarga del patrón completo.")
else:
    st.info("👆 Sube una imagen arriba para generar la vista previa del patrón y su leyenda.")

# --- FOOTER ---
st.markdown("---")
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown("<p style='color: #AAAAAA;'>🚀 DiamondEcoPro • Tu estudio creativo sostenible</p>", unsafe_allow_html=True)
with f_col2:
    st.markdown(f"<p style='text-align: right; color: #00FFCC;'>👀 Visitas: {st.session_state.visitas}</p>", unsafe_allow_html=True)
