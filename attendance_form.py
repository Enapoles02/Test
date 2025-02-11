import streamlit as st
import pandas as pd
import os
from urllib.parse import quote
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

# --- Configuración inicial ---
st.set_page_config(page_title="Daily Huddle", layout="centered")

# --- Función para detectar si estamos en Streamlit Cloud o Local ---
def get_base_url():
    """ Detecta automáticamente la URL base (local o en Streamlit Cloud). """
    try:
        host = st.request.host
        if "localhost" in host:
            return "http://localhost:8501"
        else:
            return f"https://{host}"
    except:
        return "http://localhost:8501"  # En caso de error, usa localhost

# --- Función para generar la URL del usuario ---
def generate_user_url(username):
    """ Genera la URL personalizada para cada usuario. """
    base_url = get_base_url()
    return f"{base_url}/?user={quote(username.strip())}"

# --- Manejo de claves AES ---
KEY_FILE = "key.key"
if not os.path.exists(KEY_FILE):
    # Generar y guardar la clave si no existe
    KEY = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(KEY)
else:
    # Cargar la clave existente
    with open(KEY_FILE, "rb") as key_file:
        KEY = key_file.read()

cipher = Fernet(KEY)

# --- Variables globales ---
MASTER_TEAM_LEAD_PASSWORD = "MasterTeamLead123"  # Contraseña de un solo uso

# --- Funciones auxiliares ---
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

def authenticate_user(username, password, user_db):
    user_record = user_db[user_db["Username"].str.strip().str.lower() == username.strip().lower()]
    if user_record.empty:
        return False
    stored_password = user_record["Password"].values[0]
    return decrypt_password(stored_password) == password

def load_or_create_user_db():
    try:
        return pd.read_csv("users.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Username", "Password", "URL", "Role"])

def load_or_create_attendance_db():
    try:
        return pd.read_csv("attendance.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Date", "Time", "Mood"])

def get_current_role(username):
    roles = ["Facilitator", "Action Taker", "Time Keeper", "Coach"]
    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
    role_index = hash(username + str(start_of_week)) % len(roles)
    return roles[role_index]

# --- Bases de datos ---
user_db = load_or_create_user_db()
attendance_db = load_or_create_attendance_db()

# --- Registro de usuario ---
def register_user():
    st.title("Register New User")
    with st.form("registration_form"):
        name = st.text_input("Full Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        team_lead_password = st.text_input("Team Lead Password (optional)", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif username.strip().lower() in user_db["Username"].str.strip().str.lower().values:
                st.error("Username already exists!")
            elif team_lead_password and team_lead_password != MASTER_TEAM_LEAD_PASSWORD:
                st.error("Invalid Team Lead Password!")
            else:
                role = "Team Lead" if team_lead_password == MASTER_TEAM_LEAD_PASSWORD else "User"
                encrypted_password = encrypt_password(password)
                personalized_url = generate_user_url(username)
                new_user = {"Name": name, "Username": username.strip(), "Password": encrypted_password, "URL": personalized_url, "Role": role}
                user_db.loc[len(user_db)] = new_user
                user_db.to_csv("users.csv", index=False)
                st.success(f"User registered successfully! Your personal URL is: {personalized_url}")

# --- Registro diario ---
def daily_check_in(username):
    st.title("Daily Check-In")
    role = get_current_role(username)
    st.write(f"Welcome, {username}")
    st.write(f"Your role for this week is: **{role}**")

    with st.form("daily_checkin_form"):
        mood = st.radio("How are you feeling today?", ["😊 Happy", "😐 Neutral", "😞 Stressed"], horizontal=True)
        submit = st.form_submit_button("Submit")

        if submit:
            now = datetime.now()
            date_today = now.strftime("%Y-%m-%d")
            time_now = now.strftime("%H:%M:%S")
            new_entry = {"Username": username, "Date": date_today, "Time": time_now, "Mood": mood}
            attendance_db.loc[len(attendance_db)] = new_entry
            attendance_db.to_csv("attendance.csv", index=False)
            st.success("Your check-in has been recorded!")

# --- Tablero general ---
def admin_dashboard(username):
    role = user_db[user_db["Username"].str.strip().str.lower() == username.strip().lower()]["Role"].values[0]
    if role != "Action Taker" and role != "Team Lead":
        st.error("You do not have permission to access this page.")
        return

    st.title("Admin Dashboard")
    st.subheader("Today's Attendance")

    today = datetime.now().strftime("%Y-%m-%d")
    today_data = attendance_db[attendance_db["Date"] == today]

    if not today_data.empty:
        st.dataframe(today_data)
    else:
        st.info("No attendance records for today.")

# --- Enrutamiento ---
st.sidebar.title("Navigation")
query_params = st.query_params
username = query_params.get("user", None)

if username:
    username = username.strip().lower()
    registered_users = user_db["Username"].str.strip().str.lower().tolist()

    if username in registered_users:
        daily_check_in(username)
    else:
        st.error("Invalid user parameter in URL.")
else:
    option = st.sidebar.selectbox("Choose a page", ["Register", "Login"])

    if option == "Register":
        register_user()
    elif option == "Login":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if authenticate_user(username, password, user_db):
                    user_record = user_db[user_db["Username"].str.strip().str.lower() == username.strip().lower()]
                    if not user_record.empty:
                        personalized_url = user_record["URL"].values[0]
                        st.success("Login successful! Redirecting...")
                        st.write(f"[Click here to go to your page]({personalized_url})")
                    else:
                        st.error("User found in login but URL retrieval failed.")
                else:
                    st.error("Invalid username or password.")
