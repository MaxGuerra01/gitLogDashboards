import json
from pathlib import Path

with open("git_log_completo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

html = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Dashboard Git Log</title>
  <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
</head>
<body>
  <h1>📊 Dashboard Git (por commit)</h1>
  <div id="chart"></div>
  <script>
    const data = __DATA__;

    const porFecha = {};
    data.forEach(commit => {
      const fecha = commit.date.split("T")[0];
      porFecha[fecha] = (porFecha[fecha] || 0) + 1;
    });

    const fechas = Object.entries(porFecha).sort((a,b) => new Date(a[0]) - new Date(b[0]));
    const chart = new ApexCharts(document.querySelector("#chart"), {
      chart: { type: 'line' },
      title: { text: 'Commits por Fecha' },
      series: [{ name: 'Commits', data: fechas.map(f => f[1]) }],
      xaxis: { categories: fechas.map(f => f[0]) }
    });

    chart.render();
  </script>
</body>
</html>
"""
html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))

Path("dashboard_git_log.html").write_text(html, encoding="utf-8")
print("✅ HTML generado: dashboard_git_log.html")