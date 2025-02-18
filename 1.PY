import requests

GITHUB_USERNAME = "Enapoles02"
GITHUB_TOKEN = "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"
GITHUB_API_URL = "https://api.github.com"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# 🔹 Intenta listar los repositorios para verificar que el token funciona
response = requests.get(f"{GITHUB_API_URL}/user/repos", headers=headers)

if response.status_code == 200:
    print("✅ Token válido. Repositorios encontrados:")
    print([repo["name"] for repo in response.json()])
else:
    print(f"❌ ERROR: {response.status_code} - {response.json()}")
