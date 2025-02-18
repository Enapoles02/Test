import requests
import os

# Carga los valores desde GitHub Secrets
GITHUB_CLIENT_ID = os.getenv("MY_GITHUB_APP_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("MY_GITHUB_APP_CLIENT_SECRET")

# URL para autenticación OAuth
AUTH_URL = "https://github.com/login/oauth/access_token"
API_URL = "https://api.github.com"

def get_access_token():
    """ Obtiene un token de acceso desde la GitHub App """
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    headers = {"Accept": "application/json"}
    
    response = requests.post(AUTH_URL, data=data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Error obteniendo token: {response.text}")
        return None

def create_repository(repo_name):
    """ Crea un repositorio en GitHub usando la GitHub App """
    access_token = get_access_token()
    if not access_token:
        print("❌ No se pudo obtener un token de acceso.")
        return
    
    url = f"{API_URL}/user/repos"
    headers = {"Authorization": f"token {access_token}", "Accept": "application/vnd.github.v3+json"}
    
    data = {
        "name": repo_name,
        "private": True,
        "description": "Repositorio generado automáticamente desde GitHub App"
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print(f"✅ Repositorio '{repo_name}' creado exitosamente.")
    else:
        print(f"❌ Error creando repositorio: {response.text}")

# Prueba la creación del repositorio
if __name__ == "__main__":
    repo_name = "DailyHuddleRepo"
    create_repository(repo_name)
