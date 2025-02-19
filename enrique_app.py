
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuración de la app ---
st.set_page_config(page_title="Enrique's Daily Check-In", layout="centered")

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
st.title("Daily Check-In - Enrique")
st.write("Registra tu asistencia y estado de ánimo.")

mood = st.radio("¿Cómo te sientes hoy?", ["😊 Feliz", "😐 Neutral", "😞 Estresado"], horizontal=True)
question_response = st.radio("¿Has completado tu tarea diaria?", ["✅ Sí", "❌ No"], horizontal=True)

if st.button("Enviar"):
    save_data("Enrique", mood, question_response)
    st.success("✅ ¡Registro guardado!")
