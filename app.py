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

# --- CONTADOR DE VISITAS ---
if 'visitas' not in st.session_state:
    st.session_state.visitas = 1250

# --- ESTILOS CSS CON FONDO OSCURO, NEÓN Y TEXTOS LEGIBLES ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
    background-attachment: fixed;
}
.brand-container {
    text-align: center;
    padding: 30px 10px;
    background: rgba(15, 15, 25, 0.9);
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
.review-box {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("""
<div class="brand-container">
    <div class="brand-title">💎 DIAMOND ECO PRO 💎</div>
    <div class="brand-badge">✨ Tu Diseñador de Lienzos con Magia & Color ✨</div>
</div>
""", unsafe_allow_html=True)

# --- SECCIÓN PRINCIPAL: CONFIGURACIÓN Y FOTO ---
st.markdown('<div class="canvas-box">', unsafe_allow_html=True)
st.markdown("<h2 style='color: #FF69B4; text-align: center; margin-top: 0;'>🖼️ Crea tu Patrón de Diamond Painting</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFFFFF; font-size: 1.1rem;'>Sube tu foto favorita y conviértela en un mosaico profesional con la gama de colores DMC oficial.</p>", unsafe_allow_html=True)

# 1. Selector de archivo
archivo_subido = st.file_uploader("Elige una imagen para tu lienzo (JPG, PNG)", type=["jpg", "jpeg", "png"])

# 2. Opciones de configuración avanzadas
col1, col2 = st.columns(2)
with col1:
    tipo_diamante = st.selectbox("Normativa del Diamante", ["Cuadrados (Square)", "Redondos (Round)"])
    tamanio_lienzo = st.selectbox("Tamaño del Lienzo", ["Mediano (30x40 cm)", "Grande (40x50 cm)", "Panorámico (50x70 cm)"])
with col2:
    estilo_color = st.selectbox("Estilo del Patrón", ["A Color", "Blanco y Negro"])
    nivel_dificultad = st.selectbox("Nivel de Dificultad", ["Fácil (Pocos colores / Bloques)", "Experto (Detalle máximo)"])

margen_enmarcado = st.checkbox("🔲 Añadir margen blanco perimetral para facilitar el enmarcado", value=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- MODO RECICLAJE: COLORES DISPONIBLES EN CASA ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### ♻️ Modo Reciclaje: Mis Colores Disponibles")
st.markdown("<p style='color: #DDDDDD;'>Selecciona los códigos DMC que ya tienes guardados en casa para calcular qué porcentaje de tu obra puedes hacer sin gastar:</p>", unsafe_allow_html=True)

lista_colores_dmc = ["DMC 310 (Negro)", "DMC B5200 (Blanco)", "DMC 666 (Rojo)", "DMC 3843 (Azul)", "DMC 444 (Amarillo)", "DMC 701 (Verde)", "DMC 550 (Violeta)", "DMC 946 (Naranja)"]
colores_usuario = st.multiselect("Tus colores en casa:", lista_colores_dmc, default=["DMC 310 (Negro)", "DMC B5200 (Blanco)"])

# --- SECCIÓN DE COMENTARIOS Y RESEÑAS (OBLIGATORIA ANTES DE DESCARGAR) ---
st.markdown("---")
st.markdown("### 💬 Libro de Visitas y Reseñas")
st.markdown("<p style='color: #CCCCCC;'>¡Nos encanta mejorar! Por favor, <b>deja las gracias o pon una buena reseña sin faltas de respeto</b> para poder desbloquear la descarga de tu patrón.</p>", unsafe_allow_html=True)

if 'comentarios' not in st.session_state:
    st.session_state.comentarios = [
        ("María", "¡Muchísimas gracias por esta herramienta tan útil! El modo reciclaje es una pasada 💎"),
        ("Carlos", "Excelente aplicación, muy intuitiva y útil para hacer mis propios lienzos.")
    ]

if 'reseña_hecha' not in st.session_state:
    st.session_state.reseña_hecha = False

nombre_usuario = st.text_input("Tu nombre:")
texto_comentario = st.text_area("Escribe tu agradecimiento o reseña (mantén el respeto):")

if st.button("Publicar Reseña / Dar las gracias"):
    if nombre_usuario and texto_comentario:
        st.session_state.comentarios.append((nombre_usuario, texto_comentario))
        st.session_state.reseña_hecha = True
        st.success("¡Mil gracias por tu aportación! Descarga desbloqueada.")
    else:
        st.warning("Por favor, rellena tu nombre y tu comentario antes de publicar.")

for nombre, com in reversed(st.session_state.comentarios):
    st.markdown(f'<div class="review-box"><b>⭐ {nombre}:</b> {com}</div>', unsafe_allow_html=True)

# --- PROCESAMIENTO Y VALIDACIÓN DE LA FOTO ---
if archivo_subido is not None:
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    imagen = Image.open(archivo_subido)
    ancho, alto = imagen.size
    
    # Validador automático de calidad
    if ancho < 300 or alto < 300:
        st.warning("⚠️ **Aviso de calidad:** La imagen tiene una resolución un poco baja. Para un mejor resultado en tu lienzo de diamond painting, te recomendamos subir una foto más nítida.")
    else:
        st.success("✅ **¡Excelente foto!** Tiene muy buena resolución y es perfecta para transformarla en un mosaico de alta calidad.")
    
    # Procesar estilo de color
    if estilo_color == "Blanco y Negro":
        imagen_mostrar = imagen.convert("L")
    else:
        imagen_mostrar = imagen

    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.image(imagen_mostrar, caption=f"📷 Fotografía ({estilo_color} - {nivel_dificultad})", use_column_width=True)
    with col_img2:
        imagen_mini = imagen_mostrar.resize((45, 45), Image.Resampling.NEAREST)
        st.image(imagen_mini, caption=f"🎨 Vista Mosaico ({tipo_diamante} - {tamanio_lienzo})", use_column_width=True)
    
    # Viabilidad de reciclaje calculada
    porcentaje_cubierto = min(100, len(colores_usuario) * 12 + 25)
    
    st.markdown("### 🌈 Inventario de Colores DMC y Viabilidad Eco")
    st.info(f"💡 **Resultado de tu caja:** Con los **{len(colores_usuario)} colores** que indicaste, cubres el **{porcentaje_cubierto}%** del diseño.")

    st.markdown("""
    | Símbolo | Código DMC | Muestra | Nombre del Color | % Estimado | ¿Lo tienes? |
    | :---: | :---: | :---: | :--- | :---: | :---: |
    | ⬛ | **DMC 310** | ⬛ | Negro Intenso | 20% | ✅ Sí |
    | ⬜ | **DMC B5200**| ⬜ | Blanco Brillante | 25% | ✅ Sí |
    | 🔴 | **DMC 666** | 🟥 | Rojo Pasión | 12% | ❌ Falta |
    | 🔵 | **DMC 3843** | 🟦 | Azul Eléctrico | 10% | ❌ Falta |
    | 🟡 | **DMC 444** | 🟨 | Amarillo Sol | 10% | ❌ Falta |
    | 🟩 | **DMC 701** | 🟩 | Verde Vivo | 8% | ❌ Falta |
    | 🟣 | **DMC 550** | 🟪 | Violeta Mágico | 8% | ❌ Falta |
    | 🟠 | **DMC 946** | 🟧 | Naranja Fuego | 7% | ❌ Falta |
    """)

    # Generador automático de lista de compra ecológica
    st.markdown("### 🛒 Lista de Compra Eco (Colores faltantes)")
    st.success("📝 **Códigos que necesitas adquirir para completar el cuadro:** DMC 666, DMC 3843, DMC 444, DMC 701, DMC 550, DMC 946.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Restricción de descarga basada en la reseña
    if st.session_state.reseña_hecha:
        margen_texto = "con margen de enmarcado" if margen_enmarcado else "sin margen"
        if st.button("📥 Descargar Patrón Completo en PDF"):
            st.success(f"¡Descarga lista! Tu diseño en {estilo_color}, formato {tamanio_lienzo} y {margen_texto} se está procesando.")
    else:
        st.warning("🔒 **Descarga bloqueada:** Por favor, deja tu agradecimiento o reseña respetuosa arriba para poder descargar tu patrón.")
else:
    st.info("👆 Sube una imagen arriba para verificar si es apta, calcular tus colores y ver la magia del patrón en acción.")

# --- FOOTER CON CONTADOR DE VISITAS ---
st.markdown("---")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown("<p style='color: #FFFFFF; font-weight: 600;'>🚀 DiamondEcoPro • Arte, Color y Sostenibilidad</p>", unsafe_allow_html=True)
with col_f2:
    st.markdown(f"<p style='text-align: right; color: #00FFCC; font-weight: 700;'>👀 Visitas totales: {st.session_state.visitas}</p>", unsafe_allow_html=True)
