import streamlit as st
import os
import re

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
    text-align: center;
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

# --- LIENZO SIMULADO ---
st.markdown("""
<div class="canvas-box">
    <h3 style="color: #222222; margin-top:0;">🖼️ Tu Lienzo de Diamantes en Pantalla</h3>
    <p style="color: #666666; font-size: 0.95rem;">Mosaico interactivo listo para transformar tus fotos favoritas en patrones DMC.</p>
</div>
""", unsafe_allow_html=True)
