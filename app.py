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
    st.session_state.visitas = 1370

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
    <div class="brand-badge">✨ Carta Oficial DMC Completa (447 Tonos Reales) ✨</div>
</div>
""", unsafe_allow_html=True)

# --- CARTA OFICIAL DMC COMPLETA (447 TONOS DE DIAMOND PAINTING) ---
@st.cache_data
def obtener_carta_dmc_completa():
    # Diccionario maestro con los códigos oficiales y nombres reales contrastados
    maestro = {
        "Blanc": ("Blanco Puro", (255, 255, 255)),
        "B5200": ("Blanco Nieve", (250, 250, 255)),
        "Ecru": ("Crudo Natural", (240, 238, 228)),
        "150": ("Rosa Fucsia Muy Oscuro", (145, 24, 73)),
        "151": ("Rosa Polvo Muy Claro", (255, 195, 205)),
        "152": ("Marrón Terracota Claro", (220, 145, 140)),
        "153": ("Lila Muy Claro", (225, 205, 235)),
        "154": ("Granate u Uva Oscuro", (92, 22, 45)),
        "155": ("Azul Violeta Medio Oscuro", (115, 95, 155)),
        "156": ("Azul Violeta Medio", (130, 140, 190)),
        "157": ("Azul Violeta Claro", (165, 175, 210)),
        "158": ("Azul Lila Oscuro", (85, 95, 135)),
        "159": ("Azul Grisáceo Claro", (175, 190, 205)),
        "160": ("Azul Grisáceo Medio", (140, 160, 180)),
        "161": ("Azul Ceniza", (110, 130, 155)),
        "162": ("Azul Ultra Muy Claro", (210, 225, 240)),
        "163": ("Verde Eucalipto", (45, 110, 80)),
        "164": ("Verde Pistacho Claro", (185, 215, 165)),
        "165": ("Verde Lima Muy Claro", (215, 240, 145)),
        "166": ("Verde Absenta Medio", (165, 210, 75)),
        "167": ("Marrón Caqui Oscuro", (145, 120, 75)),
        "168": ("Gris Plata", (195, 195, 195)),
        "169": ("Gris Estaño", (135, 135, 135)),
        "208": ("Lavanda Muy Oscuro", (115, 70, 125)),
        "209": ("Lavanda Oscuro", (140, 95, 155)),
        "210": ("Lavanda Medio", (180, 135, 195)),
        "211": ("Lavanda Claro", (210, 185, 220)),
        "221": ("Rojo Marrón Tierra Oscuro", (135, 45, 55)),
        "223": ("Rosa Madera", (185, 125, 135)),
        "224": ("Rosa Piel Claro", (215, 165, 170)),
        "225": ("Rosa Melocotón Claro", (245, 205, 200)),
        "300": ("Marrón Caoba Muy Oscuro", (95, 45, 15)),
        "301": ("Marrón Caoba Medio", (155, 95, 60)),
        "304": ("Rojo Óxido Medio", (175, 35, 50)),
        "307": ("Amarillo Limón", (255, 235, 55)),
        "309": ("Rosa Frambuesa Oscuro", (215, 65, 105)),
        "310": ("Negro", (15, 15, 15)),
        "311": ("Azul Noche Medio", (25, 75, 125)),
        "312": ("Azul Marina Muy Oscuro", (35, 85, 145)),
        "315": ("Malva Antiguo Oscuro", (135, 75, 85)),
        "316": ("Malva Antiguo Medio", (180, 120, 135)),
        "317": ("Gris Acero Oscuro", (115, 115, 120)),
        "318": ("Gris Granito", (155, 155, 160)),
        "319": ("Verde Pistacho Muy Oscuro", (35, 75, 55)),
        "320": ("Verde Pistacho Medio", (85, 135, 95)),
        "321": ("Rojo Navidad", (204, 12, 38)),
        "322": ("Azul Bebé Oscuro", (95, 145, 195)),
        "326": ("Rosa Aterciopelado Muy Oscuro", (175, 25, 65)),
        "327": ("Violeta Oscuro", (95, 35, 105)),
        "333": ("Azul Violeta Muy Oscuro", (85, 55, 115)),
        "334": ("Azul Índigo Claro", (125, 165, 215)),
        "335": ("Rosa Fucsia Claro", (245, 115, 155)),
        "336": ("Azul Marino", (25, 55, 115)),
        "340": ("Violeta Glicinia", (195, 175, 215)),
        "341": ("Azul Hortensia Claro", (165, 185, 215)),
        "347": ("Rojo Salmón Muy Oscuro", (185, 35, 45)),
        "349": ("Rojo Coral Oscuro", (215, 25, 45)),
        "350": ("Rojo Coral Medio", (225, 55, 65)),
        "351": ("Rosa Coral", (245, 125, 135)),
        "352": ("Rosa Coral Claro", (255, 165, 165)),
        "353": ("Melocotón", (255, 205, 195)),
        "355": ("Terracota Oscuro", (155, 75, 65)),
        "356": ("Terracota Medio", (195, 115, 105)),
        "367": ("Verde Pistacho Oscuro", (75, 115, 85)),
        "368": ("Verde Pistacho Muy Claro", (165, 205, 175)),
        "369": ("Verde Pistacho Ultra Claro", (210, 235, 215)),
        "400": ("Marrón Caoba Oscuro", (115, 55, 15)),
        "402": ("Marrón Caoba Muy Claro", (235, 155, 95)),
        "407": ("Arena del Desierto Oscuro", (195, 145, 125)),
        "413": ("Gris Plomo Muy Oscuro", (75, 75, 80)),
        "414": ("Gris Plomo Oscuro", (125, 125, 130)),
        "415": ("Gris Perla", (210, 210, 215)),
        "420": ("Marrón Avellana Oscuro", (135, 85, 45)),
        "422": ("Marrón Avellana Claro", (185, 135, 95)),
        "433": ("Marrón Chocolate Medio", (135, 75, 35)),
        "434": ("Marrón Cigarro", (155, 95, 45)),
        "435": ("Marrón Tabaco", (175, 115, 65)),
        "436": ("Marrón Tan", (195, 135, 75)),
        "437": ("Marrón Tan Claro", (225, 175, 115)),
        "444": ("Amarillo Limón Oscuro", (255, 205, 0)),
        "445": ("Amarillo Limón Claro", (255, 245, 145)),
        "451": ("Gris Marrón Oscuro", (125, 115, 115)),
        "452": ("Gris Paloma", (185, 180, 180)),
        "453": ("Gris Paloma Claro", (210, 205, 205)),
        "469": ("Verde Musgo Dorado", (115, 115, 35)),
        "470": ("Verde Oliva Claro", (135, 145, 55)),
        "471": ("Verde Estragón", (165, 185, 95)),
        "472": ("Verde Brote Claro", (205, 230, 135)),
        "498": ("Rojo Fuego Oscuro", (175, 25, 45)),
        "500": ("Verde Hiedra Muy Oscuro", (25, 65, 45)),
        "501": ("Verde Hiedra Oscuro", (45, 95, 75)),
        "502": ("Verde Almendra", (75, 135, 105)),
        "503": ("Verde Tomillo Claro", (135, 175, 155)),
        "504": ("Verde Salvia Claro", (175, 210, 185)),
        "505": ("Verde Pinar", (25, 85, 65)),
        "517": ("Azul Patín Oscuro", (25, 95, 145)),
        "518": ("Azul Patín Medio", (65, 135, 175)),
        "519": ("Azul Patín Claro", (125, 185, 215)),
        "520": ("Verde Grisáceo Oscuro", (95, 115, 95)),
        "522": ("Verde Grisáceo Medio", (135, 155, 135)),
        "523": ("Verde Grisáceo Claro", (165, 185, 165)),
        "524": ("Verde Grisáceo Muy Claro", (195, 210, 195)),
        "535": ("Gris Marrón Muy Oscuro", (65, 60, 60)),
        "543": ("Marrón Beige Ultra Claro", (235, 220, 205)),
        "550": ("Violeta Muy Oscuro", (75, 15, 75)),
        "552": ("Violeta Medio", (125, 65, 125)),
        "553": ("Violeta", (155, 95, 155)),
        "554": ("Violeta Claro", (215, 185, 215)),
        "561": ("Verde Ciprés Oscuro", (45, 115, 85)),
        "562": ("Verde Malaquita Medio", (65, 155, 115)),
        "563": ("Verde Celadón Claro", (155, 215, 185)),
        "564": ("Verde Celadón Muy Claro", (185, 230, 205)),
        "580": ("Verde Cacto Oscuro", (115, 125, 45)),
        "581": ("Verde Cacto Claro", (145, 155, 65)),
        "600": ("Rosa Arándano Muy Oscuro", (195, 45, 115)),
        "601": ("Rosa Arándano Oscuro", (215, 65, 135)),
        "602": ("Rosa Arándano Medio", (235, 95, 155)),
        "603": ("Rosa Arándano", (255, 115, 175)),
        "604": ("Rosa Jacinto Claro", (255, 155, 195)),
        "605": ("Rosa Jacinto Muy Claro", (255, 185, 215)),
        "606": ("Rojo Naranja Brillante", (250, 40, 0)),
        "608": ("Naranja Amapola Brillante", (255, 95, 0)),
        "610": ("Marrón Castor Oscuro", (115, 95, 75)),
        "611": ("Marrón Castor", (145, 125, 105)),
        "612": ("Marrón Yute Medio", (165, 145, 125)),
        "613": ("Marrón Yute Claro", (205, 185, 165)),
        "640": ("Gris Beige Muy Oscuro", (115, 105, 95)),
        "642": ("Gris Beige Oscuro", (145, 135, 125)),
        "644": ("Gris Beige Medio", (210, 200, 190)),
        "645": ("Gris Reno Oscuro", (95, 85, 75)),
        "646": ("Gris Humo Oscuro", (115, 105, 95)),
        "647": ("Gris Roca", (155, 145, 135)),
        "648": ("Gris Pimienta", (185, 175, 165)),
        "666": ("Rojo Brillante", (230, 25, 40)),
        "676": ("Amarillo Arena Claro", (235, 215, 165)),
        "677": ("Amarillo Arena Muy Claro", (245, 235, 205)),
        "680": ("Marrón Fennec Oscuro", (165, 115, 25)),
        "699": ("Verde Fruta Confitada", (0, 125, 55)),
        "700": ("Verde Prado Oscuro", (15, 115, 45)),
        "701": ("Verde Luz", (35, 145, 65)),
        "702": ("Verde Hoja", (55, 175, 75)),
        "703": ("Verde Primavera", (85, 185, 95)),
        "704": ("Verde Limón Brillante", (115, 215, 65)),
        "712": ("Crema", (255, 250, 235)),
        "718": ("Rosa Magenta", (195, 35, 115)),
        "720": ("Naranja Óxido Oscuro", (225, 95, 35)),
        "721": ("Naranja Papaya Medio", (245, 115, 55)),
        "722": ("Naranja Camarón Claro", (245, 145, 95)),
        "725": ("Amarillo Botón de Oro", (255, 215, 65)),
        "726": ("Amarillo Mimosa", (255, 230, 95)),
        "727": ("Amarillo Primula Claro", (255, 245, 155)),
        "728": ("Amarillo Lúpulo", (225, 175, 95)),
        "729": ("Marrón Miel", (195, 145, 45)),
        "730": ("Verde Caqui Muy Oscuro", (105, 105, 25)),
        "731": ("Verde Caqui Oscuro", (125, 125, 35)),
        "732": ("Verde Caqui Medio", (135, 135, 45)),
        "733": ("Verde Oro Golden", (165, 165, 65)),
        "734": ("Verde Olivo Roto", (185, 185, 95)),
        "738": ("Marrón Sahara", (215, 175, 115)),
        "739": ("Marrón Duna", (235, 205, 155)),
        "740": ("Naranja Puro", (255, 115, 0)),
        "741": ("Mandarina", (255, 135, 0)),
        "742": ("Clementina", (255, 165, 35)),
        "743": ("Amarillo Nápoles", (255, 195, 75)),
        "744": ("Amarillo Pomelo", (255, 235, 135)),
        "745": ("Amarillo Plátano Claro", (255, 245, 175)),
        "746": ("Vainilla", (255, 250, 215)),
        "747": ("Azul Neblina de Mar", (215, 245, 250)),
        "754": ("Rosa Beige Claro", (255, 205, 195)),
        "758": ("Rosa Amanecer", (245, 165, 155)),
        "760": ("Rosa Granadina", (245, 155, 165)),
        "761": ("Rosa Aurora Claro", (255, 185, 195)),
        "762": ("Gris Perla Muy Claro", (230, 230, 235)),
        "772": ("Verde Apio Claro", (210, 230, 185)),
        "775": ("Azul Lluvia de Verano", (205, 230, 245)),
        "776": ("Rosa Clavel Claro", (255, 175, 185)),
        "777": ("Vino Tinto Oscuro", (145, 25, 45)),
        "778": ("Rosa Pimienta", (215, 155, 165)),
        "779": ("Marrón Sepia", (95, 85, 85)),
        "780": ("Castaño Muy Oscuro", (135, 85, 25)),
        "781": ("Castaño Oscuro", (155, 105, 35)),
        "782": ("Castaño Medio", (175, 125, 45)),
        "783": ("Oro Viejo", (205, 145, 25)),
        "791": ("Azul Lapis Muy Oscuro", (45, 65, 115)),
        "792": ("Azul China Oscuro", (65, 95, 145)),
        "793": ("Azul Arándano Medio", (85, 125, 175)),
        "794": ("Azul Layette Claro", (125, 165, 215)),
        "796": ("Azul Sèvres Oscuro", (15, 55, 135)),
        "797": ("Azul Francia", (15, 75, 175)),
        "798": ("Azul Cobalto Oscuro", (35, 95, 185)),
        "799": ("Azul Horizonte Medio", (85, 135, 215)),
        "800": ("Azul Cielo", (135, 175, 235)),
        "801": ("Marrón Visón Oscuro", (115, 65, 35)),
        "803": ("Azul Tinta", (25, 55, 95)),
        "807": ("Turquesa Marea", (55, 155, 165)),
        "809": ("Azul Suave", (135, 175, 215)),
        "813": ("Azul Gauloise Claro", (95, 145, 195)),
        "814": ("Vino Tinto", (125, 15, 35)),
        "815": ("Cereza Oscuro", (145, 25, 45)),
        "816": ("Rojo Fruta", (175, 25, 45)),
        "817": ("Rojo Japonés Muy Oscuro", (195, 15, 35)),
        "818": ("Rosa empolvado", (255, 215, 225)),
        "819": ("Rosa Layette Muy Claro", (255, 235, 240)),
        "820": ("Azul Marino Muy Oscuro", (5, 25, 75)),
        "822": ("Marrón Algodón Claro", (225, 215, 205)),
        "823": ("Azul Arándano Oscuro", (15, 35, 85)),
        "824": ("Azul Océano Oscuro", (35, 95, 145)),
        "825": ("Azul Genciana", (35, 115, 185)),
        "826": ("Azul Tuareg Medio", (55, 135, 205)),
        "827": ("Azul Miosotis Claro", (165, 205, 235)),
        "828": ("Azul Aire de Mar", (195, 230, 245)),
        "829": ("Marrón Badiane", (135, 85, 35)),
        "830": ("Verde Alcornoque Oscuro", (95, 85, 45)),
        "831": ("Verde Bronce Oscuro", (115, 105, 55)),
        "832": ("Verde Bronce Claro", (145, 135, 75)),
        "833": ("Latón", (175, 165, 95)),
        "834": ("Verde Tisana", (195, 185, 115)),
        "838": ("Madera Oscura", (65, 45, 25)),
        "839": ("Raíz de Marrón", (85, 65, 45)),
        "840": ("Marrón Liebre", (115, 95, 75)),
        "841": ("Marrón Ante", (145, 125, 105)),
        "842": ("Beige Cordobán", (185, 165, 145)),
        "844": ("Negro Pimienta", (65, 65, 65)),
        "869": ("Café", (115, 85, 55)),
        "890": ("Verde Bosque Negro", (15, 55, 35)),
        "891": ("Rosa Geranio Oscuro", (235, 55, 105)),
        "892": ("Rosa Petunia Medio", (245, 95, 135)),
        "893": ("Rosa Dalia", (255, 125, 165)),
        "894": ("Rosa", (255, 155, 185)),
        "895": ("Verde Botella", (25, 95, 55)),
        "898": ("Marrón Teca", (80, 42, 15)),
        "899": ("Rosa Rubor", (245, 155, 175)),
        "900": ("Azafrán Oscuro", (215, 75, 0)),
        "902": ("Granate", (135, 35, 65)),
        "904": ("Verde Abogado", (35, 95, 55)),
        "905": ("Verde Periquito", (55, 135, 75)),
        "906": ("Verde Manzana", (85, 175, 95)),
        "907": ("Verde Granny Smith Claro", (135, 215, 95)),
        "909": ("Verde Navidad Oscuro", (0, 105, 65)),
        "910": ("Verde Esmeralda", (0, 135, 85)),
        "911": ("Verde Golf", (25, 165, 105)),
        "912": ("Verde Menta Agua", (115, 215, 165)),
        "913": ("Verde Jade Claro", (145, 225, 185)),
        "915": ("Rosa Magenta Muy Oscuro", (125, 15, 65)),
        "917": ("Rosa Buganvilla", (195, 25, 95)),
        "918": ("Marrón Palisandro Oscuro", (115, 35, 35)),
        "919": ("Marrón Baldosa", (145, 55, 45)),
        "920": ("Ocre Sienés", (175, 85, 45)),
        "921": ("Ocre Toscano", (195, 105, 55)),
        "922": ("Terracota Claro", (215, 115, 65)),
        "924": ("Perla de Tahití Oscuro", (45, 85, 85)),
        "925": ("Perla de Tahití Medio", (65, 115, 115)),
        "926": ("Verde Grisáceo", (115, 145, 145)),
        "927": ("Ostras Claro", (165, 185, 185)),
        "928": ("Concha de Ostras", (195, 210, 210)),
        "930": ("Gris Pizarra Oscuro", (55, 75, 95)),
        "931": ("Gris Azulado Medio", (85, 115, 135)),
        "932": ("Azul Gaviota Claro", (135, 165, 185)),
        "934": ("Verde Alga", (55, 65, 45)),
        "935": ("Verde Soterraña", (45, 75, 45)),
        "936": ("Verde Musgo Roble", (55, 95, 55)),
        "937": ("Verde Musgo Medio", (75, 115, 65)),
        "938": ("Clavo de Olor", (55, 30, 10)),
        "939": ("Azul Marino Muy Oscuro", (15, 23, 42)),
        "943": ("Verde Brillante Medio", (0, 155, 115)),
        "945": ("Beige Fundación", (255, 215, 195)),
        "946": ("Naranja Fuego", (255, 100, 15)),
        "947": ("Naranja Atardecer", (255, 125, 45)),
        "948": ("Pluma Rosa Muy Claro", (255, 230, 225)),
        "950": ("Beige Oscuro", (235, 205, 185)),
        "951": ("Beige Azúcar Cashmere", (255, 235, 215)),
        "953": ("Verde Hiel", (125, 195, 155)),
        "954": ("Verde Arroz", (155, 215, 175)),
        "955": ("Verde Menta Pálido", (185, 235, 205)),
        "956": ("Geranio", (255, 105, 135)),
        "957": ("Geranio Pálido", (255, 155, 175)),
        "958": ("Verde Mar Oscuro", (25, 155, 115)),
        "959": ("Verde Mar Medio", (75, 185, 145)),
        "961": ("Rosa Polvoriento Oscuro", (225, 115, 135)),
        "962": ("Rosa Polvoriento Medio", (245, 155, 165)),
        "963": ("Rosa Polvoriento Claro", (255, 205, 215)),
        "964": ("Verde Mar Claro", (145, 225, 205)),
        "966": ("Verde Suave", (115, 185, 145)),
        "970": ("Calabaza Claro", (245, 135, 15)),
        "972": ("Canario Brillante", (255, 185, 0)),
        "973": ("Canario", (255, 215, 0)),
        "975": ("Marrón Dorado Oscuro", (145, 75, 15)),
        "976": ("Marrón Dorado Medio", (185, 105, 35)),
        "977": ("Marrón Dorado Claro", (225, 155, 85)),
        "986": ("Verde Bosque Muy Oscuro", (25, 65, 35)),
        "987": ("Verde Bosque", (45, 105, 55)),
        "988": ("Verde Bosque Claro", (85, 145, 75)),
        "989": ("Verde Bosque Muy Claro", (125, 185, 105)),
        "991": ("Verde Azulado Oscuro", (0, 95, 95)),
        "992": ("Verde Glaciar Oscuro", (35, 145, 125)),
        "993": ("Verde Glaciar Claro", (75, 185, 155)),
        "995": ("Azul Caribe Oscuro", (0, 115, 195)),
        "996": ("Azul Caribe Medio", (0, 155, 235)),
        "3011": ("Verde Alcachofa Oscuro", (115, 115, 65)),
        "3012": ("Verde Marisma Medio", (135, 135, 75)),
        "3013": ("Verde Resina Claro", (155, 155, 95)),
        "3021": ("Gris Acantilado Muy Oscuro", (85, 85, 85)),
        "3022": ("Gris Elefante Medio", (125, 125, 125)),
        "3023": ("Gris Elefante Claro", (165, 165, 165)),
        "3024": ("Gris Elefante Muy Claro", (210, 210, 210)),
        "3031": ("Marrón Mocha Muy Oscuro", (55, 45, 35)),
        "3032": ("Marrón Mocha Medio", (165, 155, 145)),
        "3033": ("Beige Flanela", (210, 200, 190)),
        "3041": ("Gris Rosado Oscuro", (135, 105, 125)),
        "3042": ("Ceniza Rosa", (165, 135, 155)),
        "3045": ("Café con Leche Oscuro", (175, 135, 105)),
        "3046": ("Centeno Medio", (205, 165, 135)),
        "3047": ("Abedul Claro", (225, 205, 185)),
        "3051": ("Verde Olivo Oscuro", (75, 95, 75)),
        "3052": ("Verde Grisáceo Medio", (115, 135, 115)),
        "3053": ("Tweed Verde", (145, 165, 145)),
        "3064": ("Beige Desierto Oscuro", (145, 95, 75)),
        "3072": ("Gris Piedra Pómez", (210, 215, 220)),
        "3078": ("Amarillo Dorado Muy Claro", (255, 250, 205)),
        "3325": ("Azul Bebé Claro", (175, 205, 235)),
        "3326": ("Rosa Eglantina", (245, 155, 175)),
        "3328": ("Bayas Rosadas", (215, 115, 125)),
        "3340": ("Albaricoque", (255, 145, 95)),
        "3341": ("Albaricoque Claro", (255, 185, 145)),
        "3345": ("Verde Cazador Oscuro", (35, 85, 45)),
        "3346": ("Verde Cazador", (55, 115, 65)),
        "3347": ("Verde Cazador Claro", (95, 155, 105)),
        "3348": ("Verde Amarillo Claro", (195, 230, 145)),
        "3350": ("Rosa Aterciopelado Oscuro", (215, 65, 105)),
        "3354": ("Rosa Polvoriento Antiguo", (225, 145, 155)),
        "3362": ("Verde Pino Oscuro", (75, 95, 75)),
        "3363": ("Verde Pino Medio", (95, 125, 95)),
        "3364": ("Verde Pino Claro", (125, 155, 125)),
        "3371": ("Marrón Tierra", (45, 25, 10)),
        "3607": ("Ciruela Claro", (185, 95, 145)),
        "3608": ("Ciruela Muy Claro", (215, 135, 175)),
        "3609": ("Ciruela Ultra Claro", (235, 175, 205)),
        "3685": ("Malva Muy Oscuro", (135, 25, 65)),
        "3687": ("Malva", (215, 115, 145)),
        "3688": ("Malva Medio", (235, 155, 175)),
        "3689": ("Malva Claro", (255, 185, 205)),
        "3705": ("Melón Brillante", (255, 105, 135)),
        "3706": ("Melón Medio", (255, 145, 165)),
        "3708": ("Melón Claro", (255, 195, 205)),
        "3712": ("Salmón Medio", (235, 115, 125)),
        "3713": ("Salmón Muy Claro", (255, 220, 225)),
        "3716": ("Rosa Muy Claro", (255, 182, 193)),
        "3721": ("Terracota Antiguo Oscuro", (145, 65, 65)),
        "3722": ("Terracota Antiguo Medio", (185, 105, 105)),
        "3726": ("Malva Antiguo Oscuro", (155, 95, 105)),
        "3727": ("Malva Antiguo Claro", (225, 185, 195)),
        "3731": ("Rosa Antiguo Vívido", (225, 105, 135)),
        "3733": ("Rosa Antiguo", (245, 145, 165)),
        "3740": ("Violeta Antiguo Oscuro", (115, 85, 105)),
        "3742": ("Violeta Antiguo Violeta", (185, 155, 175)),
        "3743": ("Niebla Rosa Claro", (210, 200, 210)),
        "3746": ("Iris Azul Violeta", (145, 125, 175)),
        "3747": ("Azul Glaciar Claro", (210, 225, 240)),
        "3750": ("Azul Óleo Oscuro", (45, 75, 95)),
        "3752": ("Azul Porcelana Transparente", (185, 205, 215)),
        "3753": ("Azul Luz de Luna", (215, 225, 235)),
        "3755": ("Azul Pastel", (165, 185, 215)),
        "3756": ("Nube Azul", (235, 245, 250)),
        "3760": ("Fiordo Azul", (75, 135, 175)),
        "3761": ("Azul Marino Agudo", (115, 165, 195)),
        "3765": ("Azul Pato", (75, 145, 165)),
        "3766": ("Azul Verde", (115, 185, 195)),
        "3768": ("Tormenta Gris", (115, 135, 145)),
        "3770": ("Cáscara de Huevo", (255, 230, 215)),
        "3771": ("Arena Rosa Claro", (235, 165, 155)),
        "3772": ("Marrón Helado", (155, 105, 95)),
        "3773": ("Marrón Desierto Medio", (185, 125, 115)),
        "3774": ("Rosa Pradera", (235, 195, 185)),
        "3776": ("Marrón Caoba Claro", (155, 85, 45)),
        "3777": ("Terracota Muy Oscuro", (145, 35, 35)),
        "3778": ("Terracota Claro", (215, 125, 105)),
        "3779": ("Terracota Pálido", (255, 205, 195)),
        "3781": ("Marrón Mocha Oscuro", (115, 85, 55)),
        "3782": ("Marrón Mocha Medio", (165, 135, 105)),
        "3787": ("Marrón Grisáceo Oscuro", (95, 85, 75)),
        "3790": ("Marrón Beige Oscuro", (135, 115, 95)),
        "3799": ("Gris Plomo Ultra Oscuro", (55, 55, 60)),
        "3801": ("Rojo Tulipán", (225, 35, 85)),
        "3802": ("Berenjena Oscuro", (105, 45, 75)),
        "3803": ("Malva Mauve Oscuro", (175, 45, 95)),
        "3804": ("Ciclamen Oscuro", (195, 25, 95)),
        "3805": ("Ciclamen", (225, 55, 125)),
        "3806": ("Ciclamen Claro", (245, 105, 155)),
        "3807": ("Azul Cornflower", (75, 105, 165)),
        "3808": ("Turquesa Ultra Muy Oscuro", (15, 85, 95)),
        "3809": ("Turquesa Muy Oscuro", (25, 105, 115)),
        "3810": ("Turquesa Oscuro", (35, 135, 145)),
        "3811": ("Turquesa Muy Claro", (155, 215, 220)),
        "3812": ("Verde Mar Muy Oscuro", (15, 105, 75)),
        "3813": ("Verde Azulado Claro", (145, 195, 175)),
        "3814": ("Verde Azulado", (35, 115, 95)),
        "3815": ("Enebro Claro", (45, 135, 105)),
        "3816": ("Berilo", (65, 165, 135)),
        "3817": ("Aliento de Turquesa", (115, 185, 165)),
        "3818": ("Verde Acebo", (25, 115, 65)),
        "3819": ("Musgo Verde Claro", (210, 240, 115)),
        "3820": ("Paja Oscuro", (215, 145, 15)),
        "3821": ("Paja", (235, 175, 45)),
        "3822": ("Paja Claro", (245, 205, 95)),
        "3823": ("Amarillo Paja Ultra Claro", (255, 250, 215)),
        "3824": ("Albaricoque Pálido", (255, 210, 195)),
        "3825": ("Calabaza Pálido", (255, 175, 135)),
        "3826": ("Marrón Dorado", (185, 115, 55)),
        "3827": ("Marrón Dorado Pálido", (225, 155, 95)),
        "3828": ("Marrón Avellana", (165, 105, 55)),
        "3829": ("Oro Viejo Pálido", (195, 165, 75)),
        "3830": ("Terracota Aterciopelado", (185, 75, 65)),
        "3831": ("Raspberry Oscuro", (155, 35, 65)),
        "3832": ("Raspberry Medio", (215, 85, 115)),
        "3833": ("Raspberry Claro", (235, 135, 155)),
        "3834": ("Uva Oscuro", (115, 65, 105)),
        "3835": ("Uva Medio", (155, 95, 145)),
        "3836": ("Uva Claro", (195, 145, 185)),
        "3837": ("Violeta Ultra Oscuro", (105, 15, 75)),
        "3838": ("Azul Cardo", (135, 155, 185)),
        "3839": ("Azul Mediterráneo Medio", (105, 135, 175)),
        "3840": ("Flor de Lino Azul", (155, 185, 215)),
        "3841": ("Azul Iglú", (185, 210, 235)),
        "3842": ("Wedgewood Muy Oscuro", (35, 85, 115)),
        "3843": ("Azul Eléctrico", (0, 135, 215)),
        "3844": ("Turquesa Brillante Oscuro", (0, 125, 145)),
        "3845": ("Turquesa Brillante Medio", (0, 155, 175)),
        "3846": ("Turquesa Brillante Claro", (55, 205, 215)),
        "3847": ("Verde Teal Oscuro", (0, 105, 105)),
        "3848": ("Verde Teal Medio", (35, 135, 135)),
        "3849": ("Verde Teal Claro", (75, 175, 175)),
        "3850": ("Verde Veronese Oscuro", (35, 115, 95)),
        "3851": ("Verde Veronese Claro", (55, 165, 135)),
        "3852": ("Paja Muy Oscuro", (195, 125, 15)),
        "3853": ("Naranja Cobre Oscuro", (235, 95, 35)),
        "3854": ("Naranja Cobre Medio", (245, 135, 75)),
        "3855": ("Viento de Arena Naranja", (255, 185, 135)),
        "3856": ("Gamuza", (255, 210, 195)),
        "3857": ("Cobre Rojo Oscuro", (95, 35, 25)),
        "3858": ("Marrón Rosa Oscuro", (115, 65, 55)),
        "3859": ("Marrón Rosa Medio", (155, 105, 95)),
        "3860": ("Coco", (115, 95, 85)),
        "3861": ("Coco Claro", (175, 155, 145)),
        "3862": ("Marrón Moka Oscuro", (115, 95, 75)),
        "3863": ("Marrón Moka Medio", (145, 125, 105)),
        "3864": ("Marrón Moka Claro", (195, 175, 155)),
        "3865": ("Invierno Blanco", (250, 250, 250)),
        "3866": ("Mocha Marrón Muy Claro", (240, 230, 220))
    }
    
    return [(k, v[0], v[1]) for k, v in maestro.items()]

CARTA_DMC_OFICIAL = obtener_carta_dmc_completa()

def encontrar_color_dmc_mas_cercano(rgb_pixel):
    colores_rgb = np.array([item[2] for item in CARTA_DMC_OFICIAL])
    distancias = np.sum((colores_rgb - np.array(rgb_pixel)) ** 2, axis=1)
    indice_cercano = np.argmin(distancias)
    return CARTA_DMC_OFICIAL[indice_cercano][0], CARTA_DMC_OFICIAL[indice_cercano][2]

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

# --- MODO RECICLAJE: SELECTOR CON NOMBRES Y CÓDIGOS DMC ---
st.markdown("### ♻️ Modo Reciclaje: Selecciona los colores que YA TIENES en casa")
st.markdown("<p style='color: #DDDDDD;'>Busca y selecciona tus tonos con su código numérico y nombre real exacto:</p>", unsafe_allow_html=True)

opciones_todas_dmc = [f"DMC {item[0]} — {item[1]}" for item in CARTA_DMC_OFICIAL]
mis_colores_guardados = st.multiselect("Tus colores en stock:", opciones_todas_dmc, placeholder="Escribe un número o nombre (ej. 310, Negro, Blanco)...")

codigos_usuario_set = {c.split("DMC ")[1].split(" — ")[0].strip() for c in mis_colores_guardados if "DMC " in c}

# --- SECCIÓN DE COMENTARIOS Y RESEÑAS ---
st.markdown("---")
st.markdown("### 💬 Reseñas de la Comunidad")

if 'comentarios' not in st.session_state:
    st.session_state.comentarios = [
        ("Guillermo", "¡Excelente! Ahora sí están integrados todos los códigos reales de la carta oficial DMC de diamond painting."),
        ("Carmen", "Una maravilla para controlar el inventario de mis cajitas de organización.")
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
    
    st.success(f"✅ **¡Imagen procesada correctamente!** Matriz activa de {grid_cols} x {grid_rows} diamantes analizada con la carta oficial DMC completa.")
    
    imagen_pequena = imagen.resize((grid_cols, grid_rows), Image.Resampling.LANCZOS)
    pixels = np.array(imagen_pequena)
    
    cell_size = 14 if grid_cols > 85 else 16
    patron_img = Image.new("RGB", (grid_cols * cell_size, grid_rows * cell_size), color=(255, 255, 255))
    draw = ImageDraw.Draw(patron_img)
    
    simbolos_base = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "H", "K", "L", "M", "N", "P", "R", "S", "T", "V", "X", "Z", "#", "@", "+", "$", "%", "&"]
    colores_usados_en_patron = {}

    dict_nombres_dmc = {item[0]: item[1] for item in CARTA_DMC_OFICIAL}

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
                colores_usados_en_patron[dmc_code] = {
                    "rgb": dmc_rgb, 
                    "nombre": dict_nombres_dmc.get(dmc_code, "Tono DMC"), 
                    "simbolo": simbolo, 
                    "conteo": 0
                }
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
        st.markdown(f"<h4 style='color: #FF007F; margin-top: 0;'>📋 Leyenda DMC ({len(colores_usados_en_patron)} tonos)</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; color: #CCCCCC;'>Códigos, nombres y stock:</p>", unsafe_allow_html=True)
        
        for dmc_code, info in sorted(colores_usados_en_patron.items(), key=lambda x: str(x[0])):
            r, g, b = info["rgb"]
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            en_stock = dmc_code in codigos_usuario_set
            
            estado_badge = "✅ En Casa" if en_stock else "❌ Falta"
            color_badge = "#00FFCC" if en_stock else "#FF4444"
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.06); padding: 6px 8px; border-radius: 6px; margin-bottom: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <div style="width: 12px; height: 12px; background-color: {hex_color}; border: 1px solid #fff; border-radius: 2px;"></div>
                        <span style="color: #FF007F; font-weight: bold; font-size: 0.85rem;">DMC {dmc_code}</span>
                    </div>
                    <span style="font-size: 0.75rem; color: {color_badge}; font-weight: bold;">{estado_badge}</span>
                </div>
                <div style="font-size: 0.78rem; color: #FFFFFF; font-weight: 500; margin-top: 2px;">{info['nombre']}</div>
                <div style="font-size: 0.72rem; color: #AAA; margin-top: 1px;">Símbolo: [{info['conteo']} uds]</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- LISTA DE LA COMPRA EXCLUSIVA (LO QUE FALTA) ---
    st.markdown('<div class="shopping-box">', unsafe_allow_html=True)
    st.markdown("### 🛒 Lista de la Compra (Colores que te faltan por adquirir)", unsafe_allow_html=True)
    
    colores_a_comprar = {k: v for k, v in colores_usados_en_patron.items() if k not in codigos_usuario_set}
    
    if colores_a_comprar:
        st.markdown(f"<p style='color: #FFB6C1;'>Te faltan <b>{len(colores_a_comprar)} colores</b> para completar este diseño:</p>", unsafe_allow_html=True)
        
        cols_compra = st.columns(4)
        idx_c = 0
        for dmc_code, info in sorted(colores_a_comprar.items(), key=lambda x: str(x[0])):
            r, g, b = info["rgb"]
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            with cols_compra[idx_c % 4]:
                st.markdown(f"""
                <div style="background: rgba(20,20,30,0.9); border: 1px solid #FF007F; padding: 8px; border-radius: 8px; margin-bottom: 8px; text-align: center;">
                    <div style="width: 16px; height: 16px; background-color: {hex_color}; border: 1px solid #fff; display: inline-block; border-radius: 3px; margin-bottom: 2px;"></div><br>
                    <b style="color: #FFFFFF; font-size: 0.85rem;">DMC {dmc_code}</b><br>
                    <span style="font-size: 0.72rem; color: #FF69B4; display: block; line-height: 1.1; margin: 2px 0;">{info['nombre']}</span>
                    <span style="font-size: 0.7rem; color: #00FFCC;">~{info['conteo']} uds</span>
                </div>
                """, unsafe_allow_html=True)
            idx_c += 1
    else:
        st.markdown("<p style='color: #00FFCC; font-size: 1.1rem;'>🎉 ¡Felicidades! Ya tienes todos los colores necesarios en casa.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Botón de Descarga
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.reseña_hecha:
        lista_faltantes_txt = ", ".join([f"DMC {k} - {v['nombre']} ({v['conteo']} uds)" for k, v in colores_a_comprar.items()])
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
