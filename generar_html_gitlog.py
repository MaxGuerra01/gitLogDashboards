import json
from pathlib import Path

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Git Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
</head>
<body>
  <h1>📊 Git Log Report</h1>
  <div id="chart"></div>
  <script>
    const data = __DATA__;

    const porUsuario = {};
    const porFecha = {};
    const porArchivo = {};

    data.forEach(commit => {
      const user = commit.author;
      const fecha = commit.date.split("T")[0];
      porUsuario[user] = (porUsuario[user] || 0) + commit.archivos_modificados.reduce((s,a)=>s+a.lineas_agregadas+a.lineas_eliminadas, 0);
      porFecha[fecha] = (porFecha[fecha] || 0) + 1;
      commit.archivos_modificados.forEach(f => {
        porArchivo[f.file_path] = (porArchivo[f.file_path] || 0) + 1;
      });
    });

    const usuarios = Object.entries(porUsuario).sort((a,b)=>b[1]-a[1]);
    const fechas = Object.entries(porFecha).sort();
    const archivos = Object.entries(porArchivo).sort((a,b)=>b[1]-a[1]).slice(0,10);

    const chart = new ApexCharts(document.querySelector("#chart"), {
      chart: { type: 'bar' },
      series: [{
        name: 'Líneas modificadas',
        data: usuarios.map(x => x[1])
      }],
      xaxis: {
        categories: usuarios.map(x => x[0])
      },
      title: { text: 'Líneas modificadas por usuario' }
    });

    chart.render();
  </script>
</body>
</html>"""


def generar_html(input_json: str, output_html: str):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    contenido = TEMPLATE_HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    Path(output_html).write_text(contenido, encoding="utf-8")
    print(f"✅ HTML generado: {output_html}")


if __name__ == "__main__":
    generar_html("git_log_completo.json", "dashboard_git.html")