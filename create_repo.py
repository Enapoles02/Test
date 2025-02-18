import requests
import os

# --- CONFIGURACIÓN ---
CLIENT_ID = "Ov23liUUql4eiDC2Z3lE"  # 🔹 Tu Client ID
CLIENT_SECRET = "8e7365c5d154e1a1ae4460994268e57a9beaacbcx"  # 🔹 Tu Client Secret
AUTH_CODE = "41fb8144dce7c784c7e3"  # 🔹 Código de autorización obtenido
GITHUB_API_URL = "https://api.github.com"

# --- INTERCAMBIO DE CÓDIGO POR TOKEN ---
token_url = "https://github.com/login/oauth/access_token"
token_data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTH_CODE
}
headers = {"Accept": "application/json"}

response = requests.post(token_url, data=token_data, headers=headers)
response_data = response.json()

if "access_token" not in response_data:
    print("❌ Error obteniendo el token de acceso:", response_data)
    exit(1)

ACCESS_TOKEN = response_data["access_token"]
print("✅ Token de acceso obtenido con éxito.")

# --- CREAR REPOSITORIO ---
repo_name = "Test-Repo"  # 🔹 Cambia el nombre si lo deseas
repo_data = {
    "name": repo_name,
    "private": False,
    "description": "Repositorio creado automáticamente con OAuth"
}
headers = {
    "Authorization": f"token {ACCESS_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

repo_url = f"{GITHUB_API_URL}/user/repos"
repo_response = requests.post(repo_url, json=repo_data, headers=headers)

if repo_response.status_code == 201:
    print(f"✅ Repositorio '{repo_name}' creado exitosamente.")
    print("🔗 URL:", repo_response.json()["html_url"])
else:
    print("❌ Error creando el repositorio:", repo_response.json())
