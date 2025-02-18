import os
import requests

# 🔹 Variables de GitHub
GITHUB_USERNAME = "Enapoles02"  # Cambia esto por tu usuario en GitHub
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("❌ ERROR: No se encontró el GITHUB_TOKEN en GitHub Secrets.")
    exit(1)  # Termina el programa si no encuentra el token

print("✅ Token de GitHub detectado correctamente.")
