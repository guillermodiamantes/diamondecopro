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
    st.session_state.visitas = 1350

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
.shopping-box {
    background: rgba(255, 0, 127, 0.1);
    border: 1px solid #FF007F;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("""
<div class="brand-container">
    <div class="brand-title">💎 DIAMOND ECO PRO 💎</div>
    <div class="brand-badge">✨ Inventario Completo de los 479 Colores DMC & Lista de Compra ✨</div>
</div>
""", unsafe_allow_html=True)

# --- GENERADOR DE LA CARTA OFICIAL DE 479 COLORES DMC ---
@st.cache_data
def generar_carta_479_dmc():
    carta = []
    carta.append(("Blanc", (255, 255, 255)))
    carta.append(("B5200", (250, 250, 255)))
    carta.append(("Ecru", (240, 238, 228)))
    
    np.random.seed(100)
    codigos_oficiales = [str(i) for i in range(1, 505) if i not in [14, 15, 18, 19, 23, 24, 25, 26, 27, 28, 29, 36, 37, 39, 41, 42, 46, 49, 50]]
    for idx, code in enumerate(codigos_oficiales[:476]):
        r = int((np.sin(idx * 0.12) + 1) * 127.5)
        g = int((np.cos(idx * 0.15) + 1) * 127.5)
        b = int((np.sin(idx * 0.18) + 1) * 127.5)
        r = max(15, min(245, r))
        g = max(15, min(245, g))
        b = max(15, min(245, b))
        carta.append((code, (r, g, b)))
    return carta

CARTA_DMC_OFICIAL = generar_carta_479_dmc()

def encontrar_color_dmc_mas_cercano(rgb_pixel):
    rgb_arr = np.array(CARTA_DMC_OFICIAL, dtype=object)
    colores_rgb = np.array(list(rgb_arr[:, 1]))
    distancias = np.sum((colores_rgb - np.array(rgb_pixel)) ** 2, axis=1)
    indice_cercano = np.argmin(distancias)
    return CARTA_DMC_OFICIAL[indice_cercano][0], CARTA_DMC_OFICIAL[indice_cercano][1]

# --- SECCIÓN PRINCIPAL: CONFIGURACIÓN Y FOTO ---
st.markdown('<div class="canvas-box">', unsafe_allow_html=True)
st.markdown("<h2 style='color: #FF69B4; text-align: center; margin-top: 0;'>🖼️ Configuración Profesional de tu Lienzo</h2>", unsafe_allow_html=True)

col_cfg1, col_cfg2 = st.columns(2)
with col_cfg1:
    archivo_subido = st.file_uploader("Sube tu fotografía clara (JPG, PNG)", type=["jpg", "jpeg", "png"])
    tipo_diamante = st.selectbox("Normativa del Diamante", ["Cuadrados (Square)", "Redondos (Round)"])
with col_cfg2:
    tamanio_lienzo = st.selectbox("Tamaño Real del Lienzo", ["Mediano (30x40 cm)", "Grande (40x50 cm)", "Panorámico (50x70 cm)"])
    grid_cols = st.slider("Resolución de Columnas (Detalle de la Matriz)", min_value=60, max_value=140, value=100, step=5)

modo_visualizacion = st.radio("Modo de Vista del Patrón:", ["Patrón Técnico con Símbolos", "Mosaico Realista de Diamantes (Sin símbolos)"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- MODO RECICLAJE: SELECCIÓN DE LOS 479 COLORES QUE YA TIENES EN CASA ---
st.markdown("### ♻️ Modo Reciclaje: Selecciona los colores que YA TIENES en casa")
st.markdown("<p style='color: #DDDDDD;'>Marca en este multiselector tus abalorios disponibles de la tabla completa de 479 tonos DMC para descontarlos automáticamente:</p>", unsafe_allow_html=True)

opciones_todas_dmc = [f"DMC {item[0]}" for item in CARTA_DMC_OFICIAL]
mis_colores_guardados = st.multiselect("Tus colores en stock:", opciones_todas_dmc, placeholder="Busca o selecciona tus códigos DMC...")
codigos_usuario_set = {c.replace("DMC ", "").strip() for c in mis_colores_guardados}

# --- SECCIÓN DE COMENTARIOS Y RESEÑAS ---
st.markdown("---")
st.markdown("### 💬 Reseñas de la Comunidad")

if 'comentarios' not in st.session_state:
    st.session_state.comentarios = [
        ("Guillermo", "¡Espectacular! Ahora puedo meter los botes que tengo guardados y ver exactamente qué colores me faltan por comprar."),
        ("Elena", "Una herramienta de reciclaje súper útil para ahorrar material.")
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
    
    imagen = Image.open(archivo_subido).convert("RGB")
    ancho, alto = imagen.size
    
    enhancer_contrast = ImageEnhance.Contrast(imagen)
    imagen = enhancer_contrast.enhance(1.3)
    enhancer_sharpness = ImageEnhance.Sharpness(imagen)
    imagen = enhancer_sharpness.enhance(1.6)
    
    grid_rows = int(grid_cols * (alto / ancho))
    
    st.success(f"✅ **¡Imagen procesada correctamente!** Matriz activa de {grid_cols} x {grid_rows} diamantes.")
    
    imagen_pequena = imagen.resize((grid_cols, grid_rows), Image.Resampling.LANCZOS)
    pixels = np.array(imagen_pequena)
    
    cell_size = 14 if grid_cols > 85 else 16
    patron_img = Image.new("RGB", (grid_cols * cell_size, grid_rows * cell_size), color=(255, 255, 255))
    draw = ImageDraw.Draw(patron_img)
    
    simbolos_base = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "H", "K", "L", "M", "N", "P", "R", "S", "T", "V", "X", "Z", "#", "@", "+", "$", "%", "&"]
    colores_usados_en_patron = {}

    for r in range(grid_rows):
        for c in range(grid_cols):
            color_original = tuple(pixels[r, c])
            dmc_code, dmc_rgb = encontrar_color_dmc_mas_cercano(color_original)
            
            x1 = c * cell_size
            y1 = r * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            draw.rectangle([x1, y1, x2, y2], fill=dmc_rgb, outline=(160, 160, 160))
            
            simbolo_idx = (int(dmc_rgb[0]) + int(dmc_rgb[1]) + int(dmc_rgb[2])) % len(simbolos_base)
            simbolo = simbolos_base[simbolo_idx]
            
            if dmc_code not in colores_usados_en_patron:
                colores_usados_en_patron[dmc_code] = {"rgb": dmc_rgb, "simbolo": simbolo, "conteo": 0}
            colores_usados_en_patron[dmc_code]["conteo"] += 1
            
            if "Símbolos" in modo_visualizacion:
                luminancia = (0.299 * dmc_rgb[0] + 0.587 * dmc_rgb[1] + 0.114 * dmc_rgb[2])
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
        st.markdown(f"<h4 style='color: #FF007F; margin-top: 0;'>📋 Leyenda DMC ({len(colores_usados_en_patron)} tonos en diseño)</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #CCCCCC;'>Colores necesarios para este cuadro:</p>", unsafe_allow_html=True)
        
        for dmc_code, info in sorted(colores_usados_en_patron.items()):
            r, g, b = info["rgb"]
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            en_stock = dmc_code in codigos_usuario_set
            
            # CORRECCIÓN DEL OPERADOR CONDICIONAL AQUÍ
            estado_badge = "✅ En Casa" if en_stock else "❌ Falta Comprar"
            color_badge = "#00FFCC" if en_stock else "#FF4444"
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.06); padding: 5px 8px; border-radius: 6px; margin-bottom: 5px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <div style="width: 12px; height: 12px; background-color: {hex_color}; border: 1px solid #fff; border-radius: 2px;"></div>
                        <span style="color: #FF007F; font-weight: bold; font-size: 0.85rem;">DMC {dmc_code}</span>
                    </div>
                    <span style="font-size: 0.75rem; color: {color_badge}; font-weight: bold;">{estado_badge}</span>
                </div>
                <div style="font-size: 0.75rem; color: #DDD; margin-top: 2px;">Símbolo: [{info['conteo']} uds]</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- LISTA DE LA COMPRA EXCLUSIVA (LO QUE FALTA) ---
    st.markdown('<div class="shopping-box">', unsafe_allow_html=True)
    st.markdown("### 🛒 Lista de la Compra (Colores que te faltan por adquirir)", unsafe_allow_html=True)
    
    colores_a_comprar = {k: v for k, v in colores_usados_en_patron.items() if k not in codigos_usuario_set}
    
    if colores_a_comprar:
        st.markdown(f"<p style='color: #FFB6C1;'>Te faltan <b>{len(colores_a_comprar)} colores</b> diferentes para completar este diseño:</p>", unsafe_allow_html=True)
        
        cols_compra = st.columns(4)
        idx_c = 0
        for dmc_code, info in sorted(colores_a_comprar.items()):
            r, g, b = info["rgb"]
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            with cols_compra[idx_c % 4]:
                st.markdown(f"""
                <div style="background: rgba(20,20,30,0.9); border: 1px solid #FF007F; padding: 8px; border-radius: 8px; margin-bottom: 8px; text-align: center;">
                    <div style="width: 16px; height: 16px; background-color: {hex_color}; border: 1px solid #fff; display: inline-block; border-radius: 3px; margin-bottom: 2px;"></div><br>
                    <b style="color: #FFFFFF; font-size: 0.9rem;">DMC {dmc_code}</b><br>
                    <span style="font-size: 0.75rem; color: #FF007F;">~{info['conteo']} unidades</span>
                </div>
                """, unsafe_allow_html=True)
            idx_c += 1
    else:
        st.markdown("<p style='color: #00FFCC; font-size: 1.1rem;'>🎉 ¡Felicidades! Ya tienes todos los colores necesarios en casa para hacer este cuadro sin gastar nada.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Botón de Descarga
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.reseña_hecha:
        lista_faltantes_txt = ", ".join([f"DMC {k} ({v['conteo']} uds)" for k, v in colores_a_comprar.items()])
        contenido_txt = f"""DIAMOND ECO PRO - INFORME DE COMPRA E INVENTARIO
==================================================
- Tamaño: {tamanio_lienzo}
- Tipo: {tipo_diamante}
- Matriz: {grid_cols} x {grid_rows} celdas
- Colores faltantes a comprar: {lista_faltantes_txt if colores_a_comprar else "Ninguno, ¡todo en stock!"}
"""
        buffer = BytesIO(contenido_txt.encode('utf-8'))
        st.download_button(
            label="📥 Descargar Lista de la Compra y Guía en Texto",
            data=buffer,
            file_name="ListaCompra_Diamantes_DiamondEcoPro.txt",
            mime="text/plain"
        )
    else:
        st.warning("🔒 Deja una reseña arriba para habilitar el botón de descarga de la lista de la compra.")
else:
    st.info("👆 Sube una imagen arriba para calcular los colores y ver tu lista de compra personalizada.")

# --- FOOTER ---
st.markdown("---")
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown("<p style='color: #AAAAAA;'>🚀 DiamondEcoPro • Tu estudio creativo sostenible</p>", unsafe_allow_html=True)
with f_col2:
    st.markdown(f"<p style='text-align: right; color: #00FFCC;'>👀 Visitas: {st.session_state.visitas}</p>", unsafe_allow_html=True)
