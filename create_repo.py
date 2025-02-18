import os
import requests

# 🔹 Cargar credenciales desde GitHub Secrets
GITHUB_CLIENT_ID = os.getenv("MY_GITHUB_APP_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("MY_GITHUB_APP_CLIENT_SECRET")
GITHUB_USERNAME = "Enapoles02"  # 🔹 Reemplázalo con tu usuario de GitHub

# 🔹 Depuración: Verifica si las variables están bien cargadas
print(f"GITHUB_CLIENT_ID: {GITHUB_CLIENT_ID}")
print(f"GITHUB_CLIENT_SECRET: {'SET' if GITHUB_CLIENT_SECRET else 'NOT SET'}")

if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
    raise ValueError("❌ ERROR: No se encontró el GITHUB_CLIENT_ID o GITHUB_CLIENT_SECRET en GitHub Secrets.")

# 🔹 URL para obtener el token de acceso usando la GitHub App
GITHUB_OAUTH_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_URL = "https://api.github.com"

# 🔹 Solicitar el token de acceso con la GitHub App
def get_github_access_token():
    print("🔄 Solicitando token de acceso desde GitHub...")
    response = requests.post(
        GITHUB_OAUTH_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        if access_token:
            print("✅ Token obtenido correctamente.")
            return access_token
        else:
            print(f"❌ Error en respuesta: {response.json()}")
            raise ValueError("❌ No se encontró access_token en la respuesta.")
    else:
        print(f"❌ Error obteniendo token: {response.json()}")
        raise ValueError("❌ No se pudo obtener un token de acceso.")

# 🔹 Token de acceso
GITHUB_ACCESS_TOKEN = get_github_access_token()

# 🔹 Nombre del nuevo repositorio (puedes personalizar esto)
NEW_REPO_NAME = "DailyHuddleRepo"

# 🔹 Crear un nuevo repositorio en GitHub
def create_github_repo():
    print(f"🛠️ Creando repositorio: {NEW_REPO_NAME} en GitHub...")

    repo_data = {
        "name": NEW_REPO_NAME,
        "description": "Repositorio generado automáticamente para Daily Huddle",
        "private": True,  # 🔹 True para repos privado, False para público
        "auto_init": True,  # 🔹 Inicializa con un README.md
    }

    headers = {
        "Authorization": f"token {GITHUB_ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.post(f"{GITHUB_API_URL}/user/repos", json=repo_data, headers=headers)

    if response.status_code == 201:
        repo_url = response.json().get("html_url")
        print(f"✅ Repositorio creado exitosamente: {repo_url}")
        return repo_url
    else:
        print(f"❌ Error al crear el repositorio: {response.json()}")
        raise ValueError("❌ No se pudo crear el repositorio en GitHub.")

# 🔹 Ejecutar la creación del repositorio
if __name__ == "__main__":
    create_github_repo()
