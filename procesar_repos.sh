#!/bin/bash

set -e

JSON_FILE="repos.json"
RESULT_DIR="dataRepos"
ANALIZAR_SCRIPT="analizar_git.sh"

mkdir -p "$RESULT_DIR"

# Leer cada URL desde el JSON
jq -r '.repos[].repo_url' "$JSON_FILE" | while read -r repo_url; do
  echo "📥 Clonando: $repo_url"

  # Obtener nombre del repositorio
  repo_name=$(basename "$repo_url" .git)

  # Eliminar si ya existe la carpeta del repositorio
  if [ -d "$repo_name" ]; then
    echo "⚠️ Repositorio $repo_name ya existe. Eliminando..."
    rm -rf "$repo_name"
  fi

  # Clonar repositorio
  git clone "$repo_url" "$repo_name"

  # Entrar al repositorio
  cd "$repo_name"

  echo "🚀 Ejecutando script: $ANALIZAR_SCRIPT en $repo_name"
  bash "../$ANALIZAR_SCRIPT"

  # Obtener nombre del archivo JSON generado por analizar_git.sh
  resultado_json=$(ls *_cambios.json)

  echo "📦 Moviendo resultado a ../$RESULT_DIR/"
  mv "$resultado_json" "../$RESULT_DIR/${repo_name}_resultado.json"

  cd ..

  echo "🧹 Eliminando repositorio $repo_name"
  rm -rf "$repo_name"

done

echo "✅ Todos los repositorios fueron procesados. Resultados en: $RESULT_DIR"

# 📦 Compilar todos los JSON individuales en uno solo
echo "📊 Compilando resultados en un único archivo: $RESULT_DIR/compilado.json"

echo "[" > "$RESULT_DIR/compilado.json"
first=true

for file in "$RESULT_DIR"/*_resultado.json; do
  if [ -f "$file" ]; then
    if $first; then first=false; else echo "," >> "$RESULT_DIR/compilado.json"; fi
    cat "$file" >> "$RESULT_DIR/compilado.json"
  fi
done

echo "]" >> "$RESULT_DIR/compilado.json"

echo "✅ Archivo consolidado generado en: $RESULT_DIR/compilado.json"
