#!/bin/bash

# 📅 Fecha de inicio (pasada como argumento o por defecto)
fecha_inicio="${1:-2025-01-01}"

# 📁 Nombre del repositorio actual
repo_name=$(basename "$(git rev-parse --show-toplevel)")
output_file="${repo_name}_cambios.json"

# 🔄 Traer actualizaciones remotas
git fetch --all

# 📝 Inicializar archivo JSON
echo "" > "$output_file"
first=true

# 🔁 Recorrer todas las ramas remotas
for branch in $(git for-each-ref --format='%(refname:short)' refs/remotes/ | grep -v '\->'); do
  git checkout --quiet "$branch" || continue

  git log --since="$fecha_inicio" --pretty=format:'%H|%an|%ad|%D' --date=format:'%d-%m-%Y' --numstat | while read -r line; do

    if [[ $line =~ ^[0-9] ]]; then
      IFS=$'\t' read -r added removed filepath <<< "$line"
      if [[ -n "$filepath" && -n "$author" ]]; then
        tipo="Modificado"
        if [[ $added -gt 0 && $removed -eq 0 ]]; then tipo="Agregado"; fi
        if [[ $removed -gt 0 && $added -eq 0 ]]; then tipo="Eliminado"; fi

        if $first; then first=false; else echo "," >> "$output_file"; fi

        {
          echo -n "  {"
          echo -n "\"gitUser\": \"$author\", "
          echo -n "\"file_Path\": \"$filepath\", "
          echo -n "\"dato\": \"$tipo\", "
          echo -n "\"date_commit\": \"$date\", "
          echo -n "\"branch_name\": \"$branch\", "
          echo -n "\"lineas_agregadas\": $added, "
          echo -n "\"lineas_eliminadas\": $removed"
          echo -n "}"
        } >> "$output_file"
      fi
    elif [[ $line =~ ^[a-f0-9]{40}\| ]]; then
      IFS='|' read -r commit author date refs <<< "$line"
    fi
  done
done

# 🔚 Cierre del JSON
echo "" >> "$output_file"
echo "" >> "$output_file"

echo "✅ Reporte generado desde $fecha_inicio: $output_file"