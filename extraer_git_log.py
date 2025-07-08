import subprocess
import json
import os

def obtener_log_completo(repo_path="."):
    os.chdir(repo_path)

    # Obtener URL del repositorio remoto
    try:
        repo_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
    except subprocess.CalledProcessError:
        repo_url = "N/A"

    # Ejecutar git log con formato extendido
    cmd = [
        "git", "log", "--all", "--numstat", "--date=iso",
        "--pretty=format:⏎%H|%an|%ae|%ad|%s|%D"
    ]

    resultado = subprocess.run(cmd, capture_output=True, text=True, check=True)
    lineas = resultado.stdout.split("⏎")

    commits = []
    for bloque in lineas:
        if not bloque.strip():
            continue

        partes = bloque.strip().split("\n")
        cabecera = partes[0]
        archivos = partes[1:]

        commit_id, autor, email, fecha, mensaje, refs = cabecera.split("|", 5)
        cambios = []

        for archivo in archivos:
            if archivo.strip() == "":
                continue
            partes_arch = archivo.split("\t")
            if len(partes_arch) == 3:
                agregadas, eliminadas, ruta = partes_arch
                cambios.append({
                    "file_path": ruta,
                    "lineas_agregadas": int(agregadas) if agregadas.isdigit() else 0,
                    "lineas_eliminadas": int(eliminadas) if eliminadas.isdigit() else 0
                })

        commits.append({
            "repo_url": repo_url,
            "commit_id": commit_id,
            "author": autor,
            "email": email,
            "date": fecha,
            "message": mensaje,
            "refs": refs,
            "archivos_modificados": cambios
        })

    return commits

# === Ejecución principal ===
if __name__ == "__main__":
    datos = obtener_log_completo(".")
    with open("git_log_completo.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print("✅ Log de Git exportado a git_log_completo.json")