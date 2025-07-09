# 📊 Dashboard Git - Análisis de Cambios con ApexCharts

Este repositorio permite analizar y visualizar los cambios realizados en múltiples repositorios Git, usando Python y ApexCharts. 

---

## 🔧 Estructura de scripts

### 1. Extraer historial Git
**`extraer_git_log.py`**  
Extrae el historial completo de un repositorio Git, generando un archivo `git_log_completo.json` con:

- commit_id, autor, email, fecha, mensaje
- archivos modificados y líneas afectadas
- URL del repositorio

### 2. Procesar múltiples repositorios
**`extraer_git_log_desde_repos.py`**  
- Lee un archivo `repos.json` con URLs de repositorios
- Clona cada uno temporalmente
- Ejecuta `extraer_git_log.py` en cada uno
- Elimina las carpetas una vez procesadas

```json
{
  "repositorios": [
    { "nombre": "mi-repo", "url": "https://github.com/usuario/repo1.git" },
    { "url": "https://github.com/usuario/repo2.git" }
  ]
}
