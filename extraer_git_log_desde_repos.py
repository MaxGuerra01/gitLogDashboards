import os
import json
import shutil
import subprocess
from datetime import datetime

def clonar_y_extraer(repo_url, carpeta_destino, script_log):
    if os.path.exists(carpeta_destino):
        shutil.rmtree(carpeta_destino)

    print(f"🔄 Clonando {repo_url}...")
    subprocess.run(["git", "clone", repo_url, carpeta_destino], check=True)
    # Optionally, fetch and checkout the latest commit explicitly
    # Checkout to the latest commit on the branch with the most recent commit (regardless of branch name)
    result = subprocess.run(
        ["git", "for-each-ref", "--sort=-committerdate", "--format=%(refname:short)", "refs/heads/"],
        cwd=carpeta_destino,
        capture_output=True,
        text=True,
        check=True
    )
    latest_branch = result.stdout.strip().splitlines()[0]
    subprocess.run(["git", "checkout", latest_branch], cwd=carpeta_destino, check=True)
    subprocess.run(["git", "pull"], cwd=carpeta_destino, check=True)

    os.chdir(carpeta_destino)
    print(f"📥 Ejecutando {script_log} en {carpeta_destino}...")
    subprocess.run(["python", script_log], check=True)
    os.chdir("..")

    shutil.rmtree(carpeta_destino)
    print(f"🧹 Eliminado {carpeta_destino}.")


def procesar_repos_desde_json(archivo_json, script_log="extraer_git_log.py", base_folder="temp_repos"):
    with open(archivo_json, "r", encoding="utf-8") as f:
        repos = json.load(f)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(base_folder, exist_ok=True)
    os.chdir(base_folder)

    for repo in repos.get("repos", []):
        url = repo.get("repo_url")
        nombre = repo.get("nombre_celula", "repo_url")
        if url:
            try:
                clonar_y_extraer(url, nombre, f"../{script_log}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error procesando {url}: {e}")

    os.chdir("..")
    print("✅ Proceso completado para todos los repositorios.")


if __name__ == "__main__":
    procesar_repos_desde_json("repos.json")