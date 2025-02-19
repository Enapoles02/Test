import os

# --- CONFIGURACIÓN ---
USER_NAME = "Enrique"  # 🔹 Cambia esto dinámicamente cuando un usuario se registre
USER_FILENAME = f"{USER_NAME.lower()}_app.py"

# --- CÓDIGO BASE DE LA MINI-APP ---
user_app_code = f"""
import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuración de la app ---
st.set_page_config(page_title="{USER_NAME}'s Daily Check-In", layout="centered")

# --- Base de datos ---
CSV_FILE = "attendance_data.csv"

# --- Función para guardar datos ---
def save_data(username, mood, question_response):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = pd.DataFrame([{"Username": username, "Timestamp": now, "Mood": mood, "Question": question_response}])
    if not os.path.exists(CSV_FILE):
        data.to_csv(CSV_FILE, index=False)
    else:
        data.to_csv(CSV_FILE, mode='a', header=False, index=False)

# --- Interfaz ---
st.title("Daily Check-In - {USER_NAME}")
st.write("Registra tu asistencia y estado de ánimo.")

mood = st.radio("¿Cómo te sientes hoy?", ["😊 Feliz", "😐 Neutral", "😞 Estresado"], horizontal=True)
question_response = st.radio("¿Has completado tu tarea diaria?", ["✅ Sí", "❌ No"], horizontal=True)

if st.button("Enviar"):
    save_data("{USER_NAME}", mood, question_response)
    st.success("✅ ¡Registro guardado!")
"""

# --- GUARDAR ARCHIVO ---
with open(USER_FILENAME, "w") as user_file:
    user_file.write(user_app_code)

print(f"✅ Mini-app creada para {USER_NAME}: {USER_FILENAME}")
