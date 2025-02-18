import os
import requests

# 🔹 Variables de GitHub
GITHUB_USERNAME = "Enapoles02"  # Cambia esto por tu usuario en GitHub
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("❌ ERROR: No se encontró MY_GITHUB_TOKEN en GitHub Secrets.")

GITHUB_API_URL = "https://api.github.com"

def create_github_repo(username):
    """Crea un repositorio en GitHub para el usuario."""
    repo_name = f"streamlit_{username}"
    url = f"{GITHUB_API_URL}/user/repos"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": repo_name,
        "description": f"Repositorio de Streamlit para {username}",
        "private": False,
        "auto_init": True
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"✅ Repositorio creado con éxito: https://github.com/{GITHUB_USERNAME}/{repo_name}")
    else:
        print(f"❌ Error creando el repositorio: {response.status_code} - {response.json()}")

# 🔹 Prueba crear un repo para "Enapoles"
create_github_repo("Enapoles")
