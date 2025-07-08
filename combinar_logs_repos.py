import os
import json

def cargar_y_validar_json(path):
    objetos_validos = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            contenido = f.read()
            if contenido.strip().startswith('['):
                data = json.loads(contenido)
                if isinstance(data, list):
                    objetos_validos.extend(data)
            else:
                for linea in contenido.strip().split("\n"):
                    try:
                        obj = json.loads(linea)
                        objetos_validos.append(obj)
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"❌ Error leyendo {path}: {e}")
    return objetos_validos

def combinar_logs(directorio_base=".", nombre_salida="git_log_compilado.json"):
    todos = []
    for root, _, files in os.walk(directorio_base):
        for file in files:
            if file == "git_log_completo.json":
                ruta = os.path.join(root, file)
                print(f"🔍 Procesando {ruta}")
                todos.extend(cargar_y_validar_json(ruta))
    with open(nombre_salida, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)
    print(f"✅ Archivo combinado guardado en: {nombre_salida}")

if __name__ == "__main__":
    combinar_logs()