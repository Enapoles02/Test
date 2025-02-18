import os
import requests

# Obtener credenciales desde GitHub Secrets
GITHUB_CLIENT_ID = os.getenv("MY_GITHUB_APP_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("MY_GITHUB_APP_CLIENT_SECRET")

# URL para solicitar autenticación OAuth
AUTH_URL = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=repo"

print(f"🔹 Por favor, autoriza la aplicación en GitHub: {AUTH_URL}")
AUTH_CODE = input("🔹 Ingresa el código de autorización: ")

# Intercambiar el código de autorización por un access token
TOKEN_URL = "https://github.com/login/oauth/access_token"
token_response = requests.post(
    TOKEN_URL,
    headers={"Accept": "application/json"},
    data={
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": AUTH_CODE,
    },
)

token_data = token_response.json()
ACCESS_TOKEN = token_data.get("access_token")

if not ACCESS_TOKEN:
    print(f"❌ No se pudo obtener un token de acceso: {token_data}")
    exit()

print(f"✅ Token obtenido con éxito: {ACCESS_TOKEN[:5]}***")

# Solicitar al usuario el nombre del nuevo repositorio
REPO_NAME = input("🔹 Ingresa el nombre del nuevo repositorio: ")

# Crear el repositorio en la cuenta del usuario
REPO_URL = "https://api.github.com/user/repos"
repo_response = requests.post(
    REPO_URL,
    headers={"Authorization": f"token {ACCESS_TOKEN}", "Accept": "application/vnd.github.v3+json"},
    json={"name": REPO_NAME, "private": True},
)

if repo_response.status_code == 201:
    print(f"✅ Repositorio creado con éxito: https://github.com/{REPO_NAME}")
else:
    print(f"❌ Error al crear el repositorio: {repo_response.json()}")
