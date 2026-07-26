import streamlit as st
import os
import re

# --- CONFIGURACIÓN DE PÁGINA Y LIENZO VIRTUAL ---
st.set_page_config(
    page_title="DiamondEcoPro - Diseñador de Lienzos Gratis",
    page_icon="💎",
    layout="centered"
)

# Estilos CSS con el Nombre Súper Destacado
st.markdown("""
    <style>
    /* Fondo claro de la web */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* TITULO PRINCIPAL: Gigante, claro y con relieve */
    .brand-container {
        text-align: center;
        padding: 10px 0 20px 0;
    }

    .brand-title {
        font-size: 3.6rem;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
        background: linear-gradient(135deg, #E6007E 0%, #7F00FF 50%, #0072FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.15));
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

    /* CONTENEDOR DEL LIENZO SIMULADO */
    .canvas-container {
        background-color: #FFFFFF;
        border: 3px solid #E0E0E0;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        background-image: radial-gradient(#D0D0D0 1px, transparent 1px);
        background-size: 14px 14px;
        text-align: center;
        margin-bottom: 30px;
    }

    /* REJILLA DE DIAMANTES DE COLORES 3D */
    .mosaic-grid {
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        gap: 4px;
        max-width: 380px;
        margin: 18px auto;
        padding: 10px;
        background: #F4F4F4;
        border-radius: 10px;
        border: 2px solid #CCCCCC;
    }

    .gem {
        width: 100%;
        height: 26px;
        border-radius: 4px;
        box-shadow: inset -2px -2px 0px rgba(0,0,0,0.25), inset 2px 2px 0px rgba(255,255,255,0.8);
    }

    /* Colores DMC relucientes */
    .g-red { background-color: #FF0055; }
    .g-pink { background-color: #FF69B4; }
    .g-orange { background-color: #FF7700; }
    .g-yellow { background-color: #FFD700; }
    .g-green { background-color: #00E676; }
    .g-cyan { background-color: #00E5FF; }
    .g-blue { background-color: #2979FF; }
    .g-purple { background-color: #651FFF; }
    </style>
""", unsafe_allow_html=True)

# --- ARCHIVOS DE DATOS Y MODERACIÓN ---
COUNT_FILE = "contador_visitas.txt"
COMMENTS_FILE = "mensajes_comunidad.txt"

PALABRAS_PROHIBIDAS = [
    "puta", "puto", "mierda", "cabron", "cabrona", "gilipollas", "coño", 
    "ostia", "joder", "maricon", "hijo de puta", "pendejo", "imbecil",
    "estupido", "basura", "capullo", "maldito", "maldita", "verga"
]

def cargar_visitas():
    if not os.path.exists(COUNT_FILE):
        return 0
    with open(COUNT_FILE, "r", encoding="utf-8") as f:
        try:
            return int(f.read().strip())
        except ValueError:
            return 0

def incrementar_visita():
    visitas = cargar_visitas() + 1
    with open(COUNT_FILE, "w", encoding="utf-8") as f:
        f.write(str(visitas))
    return visitas

def buscar_palabra_fea(texto):
    texto_limpio = texto.lower()
    for palabra in PALABRAS_PROHIBIDAS:
        if re.search(r'\b' + re.escape(palabra) + r'\b', texto_limpio):
            return palabra
    return None

def guardar_mensaje(tipo, autor, texto):
    emoji = "💬" if tipo == "Agradecimiento" else "💡"
    nick = autor if autor.strip() else "Anónimo"
    with open(COMMENTS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{emoji} **{nick}** ({tipo}): \"{texto}\"\n---\n")

def cargar_mensajes():
    if not os.path.exists(COMMENTS_FILE):
        return []
    with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
        lineas = f.read().split("---\n")
        return [l.strip() for l in lineas if l.strip()]

total_visitas = incrementar_visita()

# --- CABECERA CON NOMBRE REFORZADO ---
st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">💎 DIAMOND ECO PRO 💎</h1>
    <div class="brand-badge">✨ Diseñador de Lienzos Gratis & Reciclaje Eco</div>
</div>
""", unsafe_allow_html=True)

# --- LIENZO SIMULADO ---
st.markdown("""
<div class="canvas-container">
    <h3 style="color: #222222; margin-top:0;">🖼️ Tu Lienzo de Diamantes en Pantalla</h3>
    <p style="color: #666666; font-size: 0.95rem;">Mosaico interactivo con colores de la gama oficial DMC</p>
    
    <div class="mosaic-grid">
        <div class="gem g-red"></div><div class="gem g-pink"></div><div class="gem g-orange"></div><div class="gem g-yellow"></div><div class="gem g-green"></div><div class="gem g-cyan"></div><div class="gem g-blue"></div><div class="gem g-purple"></div><div class="gem g-red"></div><div class="gem g-pink"></div><div class="gem g-orange"></div><div class="gem g-yellow"></div>
        <div class="gem g-purple"></div><div class="gem g-blue"></div><div class="gem g-cyan"></div><div class="gem g-green"></div><div class="gem g-yellow"></div><div class="gem g-orange"></div><div class="gem g-pink"></div><div class="gem g-red"></div><div class="gem g-purple"></div><div class="gem g-blue"></div><div class="gem g-cyan"></div><div class="gem g-green"></div>
        <div class="gem g-yellow"></div><div class="gem g-green"></div><div class="gem g-cyan"></div><div class="gem g-blue"></div><div class="gem g-purple"></div><div class="gem g-pink"></div><div class="gem g-red"></div><div class="gem g-orange"></div><div class="gem g-yellow"></div><div class="gem g-green"></div><div class="gem g-cyan"></div><div class="gem g-blue"></div>
    </div>

    <p style="font-size: 1.05rem; color: #444; margin-top: 15px;">
        Convierte cualquier foto en un mapa de símbolos para diamantes cuadrados o redondos y aprovecha tus sobras de casa.
    </p>
</div>
""", unsafe_allow_html=True)

# --- PASO 1: SUBIDA Y CONFIGURACIÓN ---
st.subheader("1. Configura tu Lienzo")
archivo_foto = st.file_uploader("Sube la fotografía que deseas convertir", type=["jpg", "jpeg", "png"])

if archivo_foto:
    st.info("💡 **Consejo de nitidez:** Utiliza fotos claras y enfocadas para que los detalles del lienzo queden perfectos.")
    
    tipo_diamante = st.radio(
        "Elige el tipo de diamante que vas a utilizar:",
        ["⏹️ Cuadrado (2,5 mm - Cubrimiento total)", "🔘 Redondo (2,8 mm - Colocación más rápida)"],
        horizontal=True
    )
    
    estilo_color = st.radio(
        "Elige el estilo de color:",
        ["🎨 Color Original (Gama DMC Completa)", "⚪ Escala de Grises / Blanco y Negro (Especial Reciclaje DMC 310, B5200...)"]
    )
    
    tamano = st.selectbox(
        "Selecciona el tamaño recomendado:",
        ["30 x 40 cm (~19.200 diamantes) - Ideal rostros sencillos",
         "40 x 50 cm (~32.000 diamantes) - Alta definición",
         "50 x 70 cm (~56.000 diamantes) - Máximo detalle"]
    )
    
    st.markdown("⏱️ **Tiempo estimado de montaje:** ~25 horas de diversión relajante.")
    
    # --- PASO 2: MODO RECICLAJE (ECO) ---
    st.markdown("---")
    st.subheader("2. Modo Reciclaje (Sobras DMC)")
    sobras_dmc = st.text_input("Indica las bolsas o códigos DMC que tienes en casa (opcional):", placeholder="Ej: 310 (2 bolsas), 666, B5200")
    
    if sobras_dmc:
        st.success("🟢 **Semáforo de Viabilidad: 85% Reciclable.** ¡Gran parte de tu lienzo se cubrirá con tus sobras!")

    # --- PASO 3: VISTA PREVIA ---
    st.markdown("---")
    st.subheader("3. Vista Previa del Lienzo")
    st.image(archivo_foto, caption="Vista previa de tu fotografía adaptada al patrón de diamantes", use_column_width=True)
    
    conforme = st.checkbox("He revisado la vista previa de mi cuadro y estoy conforme con el resultado.")
    
    # --- PASO 4: AGRADECIMIENTO/IDEA Y DESCARGA ---
    if conforme:
        st.markdown("---")
        st.subheader("4. ¡Ayúdanos a seguir siendo 100% Gratis!")
        st.write("Para habilitar la descarga de tu PDF, por favor déjanos unas **palabras de agradecimiento** o comparte **una idea** para mejorar la web.")
        
        tipo_mensaje = st.radio(
            "¿Qué te gustaría aportar?:",
            ["💬 Un mensaje de agradecimiento", "💡 Una idea o sugerencia para la web"],
            horizontal=True
        )
        
        nick_usuario = st.text_input("Tu Nombre o Nick (Opcional):", placeholder="Ej: Anónimo o Juan")
        
        if "agradecimiento" in tipo_mensaje:
            texto_mensaje = st.text_area("Escribe aquí tu agradecimiento:", placeholder="Ej: ¡Muchísimas gracias por crear esta herramienta tan útil!")
        else:
            texto_mensaje = st.text_area("Escribe aquí tu idea o sugerencia:", placeholder="Ej: Estaría genial añadir opción para cambiar el tamaño del texto.")
        
        if texto_mensaje.strip():
            palabra_detectada = buscar_palabra_fea(texto_mensaje) or buscar_palabra_fea(nick_usuario)
            
            if palabra_detectada:
                st.warning(f"⚠️ **Atención:** Para publicar tu mensaje y descargar el PDF, por favor elimina la palabra **\"{palabra_detectada}\"** de tu texto.")
            else:
                tipo_etiqueta = "Agradecimiento" if "agradecimiento" in tipo_mensaje else "Idea"
                
                if st.button("Enviar mi mensaje y liberar la descarga gratuita"):
                    guardar_mensaje(tipo_etiqueta, nick_usuario, texto_mensaje)
                    
                    st.markdown("---")
                    if tipo_etiqueta == "Agradecimiento":
                        st.success("💖 **¡Muchísimas gracias por tus palabras!** Gestos como el tuyo hacen que valga la pena mantener DiamondEcoPro 100% gratuita para todos. ¡Disfruta creando tu cuadro!")
                    else:
                        st.success("💡 **¡Anotamos tu idea con mucho cariño!** Gracias por ayudarnos a mejorar la web. Tu plantilla en PDF ya está lista abajo.")
                    
                    st.download_button(
                        label="📥 Descargar mi PDF Gratis Listo para Imprimir",
                        data=b"PDF_DUMMY_DATA",
                        file_name="DiamondEcoPro_Plantilla.pdf",
                        mime="application/pdf"
                    )
        else:
            st.info("✍️ Por favor, escribe tu mensaje arriba para habilitar la descarga de la plantilla.")

# --- MURO DE LA COMUNIDAD ---
st.markdown("---")
st.subheader("🌟 Muro de la Comunidad: Agradecimientos e Ideas")
mensajes = cargar_mensajes()
if mensajes:
    for m in reversed(mensajes[-6:]):
        st.markdown(m)
else:
    st.write("¡Sé el primero en dejar un agradecimiento o una idea para la web!")

# --- GUÍA DE IMPRENTAS ---
with st.expander("📖 Ver Guía de Impresión y Consejos"):
    st.markdown("""
    * **Para la Imprenta:** Imprimir el PDF en **papel adhesivo a escala 100% (tamaño real)**.
    * **Medida de la casilla:**
      * Si usas diamantes **cuadrados**: la casilla mide exactamente $2,5\\text{ mm} \\times 2,5\\text{ mm}$.
      * Si usas diamantes **redondos**: el círculo guía mide aproximadamente $2,8\\text{ mm}$.
    """)

# --- PIE Y CONTADOR ---
st.markdown("---")
st.caption(f"💎 **DiamondEcoPro** — Plataforma Gratuita | 📊 {total_visitas} visitas registradas hasta hoy.")
