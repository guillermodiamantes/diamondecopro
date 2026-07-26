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

# --- MODO RECICLAJE: CARTA COMPLETA DE COLORES DMC ENUMERADOS ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### ♻️ Modo Reciclaje: Mis Colores Disponibles")
st.markdown("<p style='color: #DDDDDD;'>Selecciona los códigos DMC que ya tienes guardados en casa de la carta completa (enumerados del 1 al 454):</p>", unsafe_allow_html=True)

# Lista completa oficial de la carta de colores DMC numerada individualmente
brutos_dmc = [
    "DMC BLANC (White)", "DMC B5200 (Snow White)", "DMC ECRU (Ecru)",
    "DMC 01 (White Tin)", "DMC 02 (Tin)", "DMC 03 (Medium Tin)", "DMC 04 (Dark Tin)",
    "DMC 05 (Light Driftwood)", "DMC 06 (Medium Light Driftwood)", "DMC 07 (Driftwood)", "DMC 08 (Dark Driftwood)", "DMC 09 (Very Dark Cocoa)",
    "DMC 10 (Very Light Tender Green)", "DMC 11 (Light Tender Green)", "DMC 12 (Tender Green)", "DMC 13 (Medium Light Nile Green)",
    "DMC 14 (Pale Apple Green)", "DMC 15 (Apple Green)", "DMC 16 (Light Chartreuse)", "DMC 17 (Light Yellow Plum)", "DMC 18 (Yellow Plum)",
    "DMC 19 (Medium Light Autumn Gold)", "DMC 20 (Shrimp)", "DMC 21 (Light Alizarin)", "DMC 22 (Alizarin)", "DMC 23 (Apple Blossom)",
    "DMC 24 (White Lavender)", "DMC 25 (Ultra Light Lavender)", "DMC 26 (Pale Lavender)", "DMC 27 (White Violet)", "DMC 28 (Medium Light Eggplant)", "DMC 29 (Eggplant)",
    "DMC 30 (Medium Light Blueberry)", "DMC 31 (Blueberry)", "DMC 32 (Dark Blueberry)", "DMC 33 (Fuchsia)", "DMC 34 (Dark Fuchsia)", "DMC 35 (Very Dark Fuchsia)",
    "DMC 150 (Dusty Rose VY DK)", "DMC 151 (Dusty Rose VY LT)", "DMC 152 (Shell Pink MED LT)", "DMC 153 (Violet VY LT)", "DMC 154 (Grape VY DK)",
    "DMC 155 (Blue Violet MED DK)", "DMC 156 (Blue Violet MED LT)", "DMC 157 (Cornflower Blue VY LT)", "DMC 158 (Cornflower Blue MED)", "DMC 159 (Grey Blue LT)",
    "DMC 160 (Grey Blue MED)", "DMC 161 (Grey Blue)", "DMC 162 (Blue ULT VY LT)", "DMC 163 (Celadon Green MED)", "DMC 164 (Forest Green LT)",
    "DMC 165 (Moss Green VY LT)", "DMC 166 (Moss Green MED LT)", "DMC 167 (Yellow Beige VY DK)", "DMC 168 (Pewter VY LT)", "DMC 169 (Pewter LT)",
    "DMC 208 (Lavender VY DK)", "DMC 209 (Lavender DK)", "DMC 210 (Lavender MED)", "DMC 211 (Lavender LT)",
    "DMC 221 (Shell Pink VY DK)", "DMC 223 (Shell Pink LT)", "DMC 224 (Shell Pink VY LT)", "DMC 225 (Shell Pink ULT VY LT)",
    "DMC 300 (Mahogany VY DK)", "DMC 301 (Mahogany MED)", "DMC 304 (Christmas Red MED)", "DMC 307 (Lemon)", "DMC 309 (Rose DEEP)", "DMC 310 (Black)",
    "DMC 311 (Navy Blue MED)", "DMC 312 (Navy Blue LT)", "DMC 315 (Antique Mauve DK)", "DMC 316 (Antique Mauve MED)", "DMC 317 (Pewter Grey)", "DMC 318 (Steel Grey LT)",
    "DMC 319 (Pistachio Green VY DK)", "DMC 320 (Pistachio Green MED)", "DMC 321 (Christmas Red)", "DMC 322 (Baby Blue DK)", "DMC 326 (Rose VY DEEP)", "DMC 327 (Violet)",
    "DMC 333 (Blue Violet VY DK)", "DMC 334 (Baby Blue MED)", "DMC 335 (Rose)", "DMC 336 (Navy Blue)", "DMC 340 (Blue Violet MED)", "DMC 341 (Blue Violet LT)",
    "DMC 347 (Salmon VY DK)", "DMC 349 (Coral DK)", "DMC 350 (Coral MED)", "DMC 351 (Coral)", "DMC 352 (Coral LT)", "DMC 353 (Peach)", "DMC 355 (Terra Cotta DK)", "DMC 356 (Terra Cotta MED)",
    "DMC 367 (Pistachio Green DK)", "DMC 368 (Pistachio Green LT)", "DMC 369 (Pistachio Green VY LT)", "DMC 370 (Mustard MED)", "DMC 371 (Mustard)", "DMC 372 (Mustard LT)",
    "DMC 400 (Mahogany DK)", "DMC 402 (Mahogany VY LT)", "DMC 407 (Clay Brown)", "DMC 413 (Pewter Grey DK)", "DMC 414 (Steel Grey DK)", "DMC 415 (Pearl Grey)",
    "DMC 420 (Hazelnut Brown DK)", "DMC 422 (Hazelnut Brown LT)", "DMC 433 (Brown MED)", "DMC 434 (Brown LT)", "DMC 435 (Brown VY LT)", "DMC 436 (Tan)", "DMC 437 (Tan LT)",
    "DMC 444 (Lemon DK)", "DMC 445 (Lemon LT)", "DMC 451 (Shell Grey DK)", "DMC 452 (Shell Grey MED)", "DMC 453 (Shell Grey LT)",
    "DMC 469 (Avocado Green)", "DMC 470 (Avocado Green LT)", "DMC 471 (Avocado Green VY LT)", "DMC 472 (Avocado Green ULT LT)", "DMC 498 (Red DK)",
    "DMC 500 (Blue Green VY DK)", "DMC 501 (Blue Green DK)", "DMC 502 (Blue Green)", "DMC 503 (Blue Green MED)", "DMC 504 (Blue Green VY LT)", "DMC 505 (Grass Green DK)",
    "DMC 517 (Wedgewood DK)", "DMC 518 (Wedgewood LT)", "DMC 519 (Sky Blue)", "DMC 520 (Fern Green DK)", "DMC 522 (Fern Green)", "DMC 523 (Fern Green LT)", "DMC 524 (Fern Green VY LT)",
    "DMC 535 (Ash Grey VY LT)", "DMC 543 (Beige Brown ULT VY LT)", "DMC 550 (Violet VY DK)", "DMC 552 (Violet MED)", "DMC 553 (Violet)", "DMC 554 (Violet LT)",
    "DMC 561 (Jade VY DK)", "DMC 562 (Jade MED)", "DMC 563 (Jade LT)", "DMC 564 (Jade VY LT)", "DMC 581 (Moss Green)", "DMC 597 (Turquoise)",
    "DMC 600 (Cranberry VY DK)", "DMC 601 (Cranberry DK)", "DMC 602 (Cranberry MED)", "DMC 603 (Cranberry)", "DMC 604 (Cranberry LT)", "DMC 605 (Cranberry VY LT)",
    "DMC 606 (Orangered BRIGHT)", "DMC 608 (Orange BRIGHT)", "DMC 610 (Drab Brown DK)", "DMC 611 (Drab Brown)", "DMC 612 (Drab Brown LT)", "DMC 613 (Drab Brown VY LT)",
    "DMC 632 (Desert Sand ULT VY DK)", "DMC 640 (Beige Grey VY DK)", "DMC 642 (Beige Grey DK)", "DMC 644 (Beige Grey MED)", "DMC 645 (Beaver Grey VY DK)",
    "DMC 646 (Beaver Grey DK)", "DMC 647 (Beaver Grey MED)", "DMC 648 (Beaver Grey LT)", "DMC 666 (Red BRIGHT)", "DMC 676 (Old Gold LT)", "DMC 677 (Old Gold VY LT)",
    "DMC 680 (Old Gold DK)", "DMC 699 (Green)", "DMC 700 (Green BRIGHT)", "DMC 701 (Green LT)", "DMC 702 (Kelly Green)", "DMC 703 (Chartreuse)", "DMC 704 (Chartreuse BRIGHT)",
    "DMC 712 (Cream)", "DMC 718 (Plum)", "DMC 720 (Orange Spice DK)", "DMC 721 (Orange Spice MED)", "DMC 722 (Orange Spice LT)", "DMC 725 (Topaz MED)", "DMC 726 (Topaz LT)",
    "DMC 727 (Topaz VY LT)", "DMC 728 (Topaz)", "DMC 729 (Old Gold MED)", "DMC 730 (Olive Green VY DK)", "DMC 731 (Olive Green DK)", "DMC 732 (Olive Green)",
    "DMC 733 (Olive Green MED)", "DMC 734 (Olive Green LT)", "DMC 738 (Tan VY LT)", "DMC 739 (Tan ULT VY LT)", "DMC 740 (Tangerine)", "DMC 741 (Tangerine MED)",
    "DMC 742 (Tangerine LT)", "DMC 743 (Yellow MED)", "DMC 744 (Yellow PALE)", "DMC 745 (Yellow LT PALE)", "DMC 746 (Off White)", "DMC 747 (Sky Blue VY LT)",
    "DMC 754 (Peach LT)", "DMC 758 (Terra Cotta VY LT)", "DMC 760 (Salmon)", "DMC 761 (Salmon LT)", "DMC 762 (Pearl Grey VY LT)", "DMC 772 (Yellow Green VY LT)",
    "DMC 775 (Baby Blue VY LT)", "DMC 776 (Pink MED)", "DMC 777 (Red DEEP)", "DMC 778 (Antique Mauve VY LT)", "DMC 779 (Brown)", "DMC 780 (Topaz ULT VY DK)",
    "DMC 781 (Topaz DK)", "DMC 782 (Topaz MED)", "DMC 783 (Topaz LT)", "DMC 791 (Cornflower Blue VY DK)", "DMC 792 (Cornflower Blue DK)", "DMC 793 (Cornflower Blue MED)",
    "DMC 794 (Cornflower Blue LT)", "DMC 796 (Royal Blue DK)", "DMC 797 (Royal Blue)", "DMC 798 (Delft Blue DK)", "DMC 799 (Delft Blue MED)", "DMC 800 (Delft Blue LT)",
    "DMC 801 (Coffee Brown DK)", "DMC 803 (Blue DEEP)", "DMC 806 (Peacock Blue DK)", "DMC 807 (Peacock Blue)", "DMC 809 (Delft Blue)", "DMC 813 (Blue LT)", "DMC 814 (Garnet DK)",
    "DMC 815 (Garnet MED)", "DMC 816 (Garnet)", "DMC 817 (Coral Red VY DK)", "DMC 818 (Baby Pink)", "DMC 819 (Baby Pink LT)", "DMC 820 (Royal Blue VY DK)",
    "DMC 822 (Beige Grey LT)", "DMC 823 (Blue DK)", "DMC 824 (Blue VY DK)", "DMC 825 (Blue DK)", "DMC 826 (Blue MED)", "DMC 827 (Blue VY LT)", "DMC 828 (Blue ULT VY LT)",
    "DMC 829 (Golden Olive VY DK)", "DMC 830 (Golden Olive DK)", "DMC 831 (Golden Olive MED)", "DMC 832 (Golden Olive)", "DMC 833 (Golden Olive LT)", "DMC 834 (Golden Olive VY LT)",
    "DMC 838 (Beige Brown VY DK)", "DMC 839 (Beige Brown DK)", "DMC 840 (Beige Brown MED)", "DMC 841 (Beige Brown LT)", "DMC 842 (Beige Brown VY LT)", "DMC 844 (Beaver Grey ULT DK)",
    "DMC 869 (Hazelnut Brown VY DK)", "DMC 890 (Pistachio Green ULT DK)", "DMC 891 (Carnation DK)", "DMC 892 (Carnation MED)", "DMC 893 (Carnation LT)", "DMC 894 (Carnation VY LT)",
    "DMC 895 (Hunter Green VY DK)", "DMC 898 (Coffee Brown VY DK)", "DMC 899 (Rose MED)", "DMC 900 (Burnt Orange DK)", "DMC 902 (Garnet VY DK)", "DMC 904 (Parrot Green VY DK)",
    "DMC 905 (Parrot Green DK)", "DMC 906 (Parrot Green MED)", "DMC 907 (Parrot Green LT)", "DMC 909 (Emerald Green VY DK)", "DMC 910 (Emerald Green DK)", "DMC 911 (Emerald Green MED)",
    "DMC 912 (Emerald Green LT)", "DMC 913 (Nile Green MED)", "DMC 915 (Plum DK)", "DMC 917 (Plum MED)", "DMC 918 (Red Copper DK)", "DMC 919 (Red Copper)", "DMC 920 (Copper MED)",
    "DMC 921 (Copper)", "DMC 922 (Copper LT)", "DMC 924 (Gray Green VY DK)", "DMC 926 (Gray Green MED)", "DMC 927 (Gray Green LT)", "DMC 928 (Gray Green VY LT)", "DMC 930 (Antique Blue DK)",
    "DMC 931 (Antique Blue MED)", "DMC 932 (Antique Blue LT)", "DMC 934 (Avocado Green BK)", "DMC 935 (Avocado Green DK)", "DMC 936 (Avocado Green VY DK)", "DMC 937 (Avocado Green MED)",
    "DMC 938 (Coffee Brown ULT DK)", "DMC 939 (Blue VY DK)", "DMC 943 (Aquamarine MED)", "DMC 945 (Tawny)", "DMC 946 (Burnt Orange MED)", "DMC 947 (Burnt Orange)", "DMC 948 (Peach VY LT)",
    "DMC 950 (Desert Sand LT)", "DMC 951 (Tawny LT)", "DMC 953 (Seagreen DK)", "DMC 954 (Seagreen MED)", "DMC 955 (Nile Green LT)", "DMC 956 (Geranium)", "DMC 957 (Geranium PALE)",
    "DMC 958 (Seagreen DK)", "DMC 959 (Seagreen MED)", "DMC 961 (Dusty Rose DK)", "DMC 962 (Dusty Rose MED)", "DMC 963 (Dusty Rose ULT VY LT)", "DMC 964 (Seagreen LT)", "DMC 966 (Baby Green MED)",
    "DMC 967 (Peach LT)", "DMC 970 (Pumpkin LT)", "DMC 971 (Pumpkin)", "DMC 972 (Canary DEEP)", "DMC 973 (Canary BRIGHT)", "DMC 975 (Golden Brown DK)", "DMC 976 (Golden Brown MED)",
    "DMC 977 (Golden Brown LT)", "DMC 986 (Forest Green VY DK)", "DMC 987 (Forest Green DK)", "DMC 988 (Forest Green MED)", "DMC 989 (Forest Green)", "DMC 991 (Aquamarine DK)", "DMC 992 (Aquamarine LT)",
    "DMC 993 (Aquamarine VY LT)", "DMC 995 (Electric Blue DK)", "DMC 996 (Electric Blue MED)",
    "DMC 3011 (Khaki Green DK)", "DMC 3012 (Khaki Green MED)", "DMC 3013 (Khaki Green LT)", "DMC 3021 (Brown Gray VY DK)", "DMC 3022 (Brown Gray MED)", "DMC 3023 (Brown Gray LT)", "DMC 3024 (Brown Gray VY LT)",
    "DMC 3031 (Mocha Brown VY DK)", "DMC 3032 (Mocha Brown MED)", "DMC 3033 (Mocha Brown VY LT)", "DMC 3041 (Antique Violet MED)", "DMC 3042 (Antique Violet LT)", "DMC 3045 (Yellow Beige DK)",
    "DMC 3046 (Yellow Beige MED)", "DMC 3047 (Yellow Beige LT)", "DMC 3051 (Green Gray DK)", "DMC 3052 (Green Gray MED)", "DMC 3053 (Green Gray LT)", "DMC 3064 (Desert Sand DK)", "DMC 3072 (Beaver Grey VY LT)",
    "DMC 3325 (Baby Blue VY LT)", "DMC 3340 (Apricot MED)", "DMC 3341 (Apricot LT)", "DMC 3345 (Hunter Green DK)", "DMC 3346 (Hunter Green)", "DMC 3347 (Hunter Green LT)", "DMC 3348 (Yellow Green LT)",
    "DMC 3350 (Dusty Rose ULT DK)", "DMC 3354 (Dusty Rose LT)", "DMC 3362 (Pine Green DK)", "DMC 3363 (Pine Green MED)", "DMC 3364 (Pine Green LT)", "DMC 3371 (Black Brown)",
    "DMC 3705 (Melon BRIGHT)", "DMC 3706 (Melon MED)", "DMC 3708 (Melon LT)", "DMC 3712 (Salmon MED)", "DMC 3713 (Salmon VY LT)", "DMC 3716 (Carnation VY LT)", "DMC 3721 (Antique Mauve VY DK)",
    "DMC 3722 (Shell Pink DK)", "DMC 3723 (Shell Pink MED)", "DMC 3724 (Antique Mauve DK)", "DMC 3726 (Antique Mauve MED)", "DMC 3727 (Antique Mauve LT)", "DMC 3731 (Dusty Rose VY DK)", "DMC 3732 (Dusty Rose MED)",
    "DMC 3733 (Dusty Rose)", "DMC 3740 (Dark Violet DK)", "DMC 3743 (Antique Violet VY LT)", "DMC 3746 (Blue Violet DK)", "DMC 3747 (Blue Violet VY LT)", "DMC 3750 (Antique Blue VY DK)", "DMC 3752 (Antique Blue VY LT)",
    "DMC 3753 (Baby Blue ULT VY LT)", "DMC 3755 (Baby Blue)", "DMC 3756 (Baby Blue ULT VY LT)", "DMC 3760 (Wedgewood MED)", "DMC 3761 (Sky Blue LT)", "DMC 3765 (Peacock Blue VY LT)", "DMC 3766 (Peacock Blue LT)",
    "DMC 3770 (Tawny VY LT)", "DMC 3771 (Terra Cotta LT)", "DMC 3772 (Terra Cotta VY DK)", "DMC 3773 (Desert Sand MED)", "DMC 3774 (Desert Sand VY LT)", "DMC 3776 (Mahogany DK)", "DMC 3778 (Terra Cotta VY LT)",
    "DMC 3779 (Terracotta VY LT)", "DMC 3781 (Mocha Brown DK)", "DMC 3782 (Mocha Brown LT)", "DMC 3787 (Brown Gray DK)", "DMC 3790 (Beige Gray ULT DK)", "DMC 3799 (Pewter Grey VY DK)",
    "DMC 3801 (Christmas Red LT)", "DMC 3802 (Antique Mauve VY DK)", "DMC 3803 (Mauve VY DK)", "DMC 3804 (Cyclamen PK DK)", "DMC 3805 (Cyclamen PK)", "DMC 3806 (Cyclamen PK LT)", "DMC 3807 (Cornflower Blue)",
    "DMC 3808 (Teal Green ULT VY DK)", "DMC 3809 (Teal Green VY DK)", "DMC 3810 (Teal Green DK)", "DMC 3811 (Turquoise VY LT)", "DMC 3812 (Seagreen VY DK)", "DMC 3813 (Blue Green LT)", "DMC 3814 (Aquamarine)",
    "DMC 3815 (Celadon Green DK)", "DMC 3816 (Celadon Green)", "DMC 3817 (Celadon Green LT)", "DMC 3818 (Emerald Green ULT VY DK)", "DMC 3819 (Moss Green LT)", "DMC 3820 (Straw DK)", "DMC 3821 (Straw)",
    "DMC 3822 (Straw LT)", "DMC 3823 (Yellow ULT PALE)", "DMC 3824 (Apricot LT)", "DMC 3825 (Pumpkin PALE)", "DMC 3826 (Golden Brown)", "DMC 3827 (Golden Brown PALE)", "DMC 3828 (Hazelnut Brown)",
    "DMC 3829 (Old Gold VY DK)", "DMC 3830 (Terra Cotta)", "DMC 3831 (Raspberry DK)", "DMC 3832 (Raspberry MED)", "DMC 3833 (Raspberry LT)", "DMC 3834 (Grape DK)", "DMC 3835 (Grape MED)",
    "DMC 3836 (Grape LT)", "DMC 3837 (Lavender ULT DK)", "DMC 3838 (Lavender Blue DK)", "DMC 3839 (Lavender Blue MED)", "DMC 3840 (Lavender Blue LT)", "DMC 3841 (Baby Blue PALE)", "DMC 3842 (Wedgewood DK)",
    "DMC 3843 (Electric Blue)", "DMC 3844 (Bright Turquoise DK)", "DMC 3845 (Bright Turquoise MED)", "DMC 3846 (Bright Turquoise LT)", "DMC 3847 (Teal Green DK)", "DMC 3848 (Teal Green MED)", "DMC 3849 (Teal Green LT)",
    "DMC 3850 (Bright Green DK)", "DMC 3851 (Bright Green LT)", "DMC 3852 (Straw VY DK)", "DMC 3853 (Autumn Gold DK)", "DMC 3854 (Autumn Gold MED)", "DMC 3855 (Autumn Gold LT)", "DMC 3856 (Mahogany ULT VY LT)",
    "DMC 3857 (Rosewood DK)", "DMC 3858 (Rosewood MED)", "DMC 3859 (Rosewood LT)", "DMC 3860 (Cocoa)", "DMC 3861 (Cocoa LT)", "DMC 3862 (Mocha Beige DK)", "DMC 3863 (Mocha Beige MED)", "DMC 3864 (Mocha Beige LT)",
    "DMC 3865 (Winter White)", "DMC 3866 (Mocha Brown ULT VY LT)"
]

# Generación automática de la lista enumerada del 1 al 454
lista_colores_dmc = [f"{i+1}. {color}" for i, color in enumerate(brutos_dmc)]

colores_usuario = st.multiselect("Tus colores en casa (Selecciona todos los que tengas):", lista_colores_dmc, default=["1. DMC BLANC (White)", "106. DMC 310 (Black)"])

# --- SECCIÓN DE COMENTARIOS Y RESEÑAS (OBLIGATORIA ANTES DE DESCARGAR) ---
st.markdown("---")
st.markdown("### 💬 Libro de Visitas y Reseñas")
st.markdown("<p style='color: #CCCCCC;'>¡Nos encanta mejorar! Por favor, <b>deja las gracias o pon una buena reseña sin faltas de respeto</b> para poder desbloquear la descarga de tu patrón.</p>", unsafe_allow_html=True)

if 'comentarios' not in st.session_state:
    st.session_state.comentarios = [
        ("María", "¡Muchísimas gracias por esta herramienta tan útil! El modo reciclaje con toda la carta DMC enumerada es increíble 💎"),
        ("Carlos", "Excelente aplicación, muy completa para organizar todos los hilos perfectamente enumerados.")
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
    
    if ancho < 300 or alto < 300:
        st.warning("⚠️ **Aviso de calidad:** La imagen tiene una resolución un poco baja. Para un mejor resultado en tu lienzo de diamond painting, te recomendamos subir una foto más nítida.")
    else:
        st.success("✅ **¡Excelente foto!** Tiene muy buena resolución y es perfecta para transformarla en un mosaico de alta calidad.")
    
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
    
    st.markdown("### 🌈 Inventario de Colores DMC y Viabilidad Eco")
    st.info(f"💡 **Resultado de tu caja:** Has seleccionado **{len(colores_usuario)} colores** enumerados de tu inventario personal para este proyecto.")

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
