import streamlit as st
import pandas as pd
import os
import requests
import base64
from urllib.parse import quote
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

# --- Configuración inicial ---
st.set_page_config(page_title="Daily Huddle", layout="centered")

# --- CREDENCIALES DE GITHUB ---
GITHUB_USERNAME = "Enapoles02"  # 🔹 Cambia esto por tu usuario de GitHub
GITHUB_TOKEN = "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"  # 🔹 Agrega tu token de GitHub aquí
GITHUB_API_URL = "https://api.github.com"

# --- FORZAR HTTPS EN STREAMLIT CLOUD ---
STREAMLIT_APP_URL_TEMPLATE = "https://{repo_name}.streamlit.app"  # 🔹 Cambia esto si es necesario

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

# --- Función para encriptar/desencriptar contraseñas ---
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

# --- Función para crear un repositorio en GitHub ---
def create_github_repo(username):
    """Crea un repositorio en GitHub para el usuario."""
    repo_name = f"streamlit_{username}"
    url = f"{GITHUB_API_URL}/user/repos"
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"name": repo_name, "private": False}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return repo_name
    else:
        return None

# --- Función para subir un archivo a GitHub ---
def upload_file_to_github(repo_name, file_path, file_content):
    """Sube un archivo al repositorio de GitHub."""
    url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_path}"
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "message": "Initial commit",
        "content": base64.b64encode(file_content.encode()).decode(),
        "branch": "main"
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    return response.status_code == 201

# --- Función para generar la URL de la aplicación en Streamlit Cloud ---
def generate_streamlit_url(repo_name):
    """Devuelve la URL de la aplicación en Streamlit Cloud."""
    return STREAMLIT_APP_URL_TEMPLATE.format(repo_name=repo_name)

# --- Función para cargar la base de datos ---
def load_or_create_user_db():
    try:
        df = pd.read_csv("users.csv", dtype=str)
        df.fillna("", inplace=True)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Username", "Password", "URL", "Role"])

def load_or_create_attendance_db():
    try:
        df = pd.read_csv("attendance.csv", dtype=str)
        df.fillna("", inplace=True)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Date", "Time", "Mood"])

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
        submit = st.form_submit_button("Register")

        if submit:
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif username.strip().lower() in user_db["Username"].astype(str).str.strip().str.lower().values:
                st.error("Username already exists!")
            else:
                # 🔹 Crear repositorio en GitHub
                repo_name = create_github_repo(username)

                if repo_name:
                    # 🔹 Subir el código al repositorio
                    file_content = open("attendance_form.py").read()
                    uploaded = upload_file_to_github(repo_name, "attendance_form.py", file_content)

                    if uploaded:
                        # 🔹 Generar la URL de la aplicación
                        personalized_url = generate_streamlit_url(repo_name)

                        # 🔹 Guardar datos en la base de datos
                        new_user = {
                            "Name": name,
                            "Username": username.strip(),
                            "Password": encrypt_password(password),
                            "URL": personalized_url,
                            "Role": "User"
                        }
                        user_db.loc[len(user_db)] = new_user
                        user_db.to_csv("users.csv", index=False)

                        st.success(f"✅ User registered successfully! Your personal URL is: {personalized_url}")
                    else:
                        st.error("❌ Error uploading files to GitHub.")
                else:
                    st.error("❌ Error creating GitHub repository.")

# --- Página de Inicio de Sesión ---
def login_user():
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            user_record = user_db[user_db["Username"].astype(str).str.strip().str.lower() == username.strip().lower()]
            if not user_record.empty:
                stored_password = decrypt_password(user_record["Password"].values[0])
                if stored_password == password:
                    personalized_url = user_record["URL"].values[0]
                    st.success("✅ Login successful! Redirecting...")
                    st.write(f"[Click here to go to your page]({personalized_url})")
                else:
                    st.error("❌ Invalid username or password.")
            else:
                st.error("❌ User not found.")

# --- Enrutamiento ---
st.sidebar.title("Navigation")
query_params = st.query_params
username = query_params.get("user", None)

if username:
    username = username.strip().lower()
    registered_users = user_db["Username"].astype(str).str.strip().str.lower().tolist()

    if username in registered_users:
        st.success(f"✅ Welcome, {username}! Access your personalized app at: {generate_streamlit_url(username)}")
    else:
        st.error("❌ Invalid user parameter in URL.")
else:
    option = st.sidebar.selectbox("Choose a page", ["Register", "Login"])

    if option == "Register":
        register_user()
    elif option == "Login":
        login_user()
