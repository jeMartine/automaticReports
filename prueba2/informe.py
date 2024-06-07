import pandas as pd
import matplotlib.pyplot as plt
import pdfkit
from docx import Document

# Cargar el archivo Excel
df = pd.read_excel('datos.xlsx')

# Crear un directorio para guardar las imágenes
import os
if not os.path.exists('graficos'):
    os.makedirs('graficos')

# Generar gráficos de barras para cada pregunta y líder
for i, row in df.iterrows():
    lider = row['Seleccione el nombre de Líder a evaluar.']
    for pregunta in df.columns[3:23]:
        evaluaciones = row[pregunta]
        if not pd.isna(evaluaciones):
            try:
                # Verificar si evaluaciones es una cadena que parece una lista
                if isinstance(evaluaciones, str) and evaluaciones.startswith('[') and evaluaciones.endswith(']'):
                    evaluaciones = eval(evaluaciones)
                # Comprobar que evaluaciones es una lista de números
                if isinstance(evaluaciones, list) and all(isinstance(x, (int, float)) for x in evaluaciones):
                    fig, ax = plt.subplots()
                    ax.bar(['Evaluador 1', 'Evaluador 2'], evaluaciones, color=['blue', 'orange'])
                    ax.set_ylim(0, 5)
                    ax.set_ylabel('Puntuación')
                    ax.set_title(f'{pregunta} - {lider}')
                    img_path = f'graficos/{lider}_{pregunta}.png'.replace(" ", "_").replace("/", "_")
                    plt.savefig(img_path)
                    plt.close()
                    df.loc[df.index[i], pregunta] = img_path
                else:
                    print(f"Datos de evaluación no válidos para {lider} en {pregunta}: {evaluaciones}")
                    df.loc[df.index[i], pregunta] = None
            except Exception as e:
                print(f"Error al evaluar los datos de {lider} en {pregunta}: {e}")
                df.loc[df.index[i], pregunta] = None

# Crear el informe HTML
html_report = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      border: 1px solid black;
      padding: 8px;
      text-align: left;
    }
    th {
      background-color: #f2f2f2;
    }
    .grafico {
      width: 100%;
      height: auto;
    }
  </style>
</head>
<body>
  <h1>Informe de Evaluación de Líderes</h1>
  <table>
    <thead>
      <tr>
        <th>Nombre del líder</th>
        <th colspan="2">Estilos de Liderazgo</th>
      </tr>
    </thead>
    <tbody>
"""

# Agregar las filas de datos al informe HTML
for i, row in df.iterrows():
    html_report += f"""
      <tr>
        <td rowspan="4">{row['Nombre del líder']}</td>
        <td colspan="2">
          <b>Estilos de Liderazgo:</b> {row['De acuerdo con los estilos de liderazgo de la Tabla anterior, ¿Cuál o cuáles considera fue el de su líder.(señale con una x una o varias opciones)']}
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <b>¿Por qué considera que su líder cumple con los Estilos de Liderazgo que usted escogió en la pregunta anterior?</b><br>
          {row['¿Por qué considera que su líder cumple con los Estilos de Liderazgo que usted escogió en la pregunta anterior? (sí contestó NINGUNO, por favor explique)']}
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <b>¿Trabajaría bajo su liderazgo en otra oportunidad?</b><br>
          {row['¿Trabajaría bajo su liderazgo en otra oportunidad?']}
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <b>¿Por qué?</b><br>
          {row['¿Por qué?']}
        </td>
      </tr>
    """
    for pregunta in df.columns[2:22]:
        if not pd.isna(row[pregunta]):
            html_report += f"""
            <tr>
              <td colspan="3">
                <img src="{row[pregunta]}" class="grafico">
              </td>
            </tr>
            """

# Cerrar el HTML
html_report += """
    </tbody>
  </table>
</body>
</html>
"""

# Guardar el informe HTML en un archivo
with open('informe.html', 'w', encoding='utf-8') as f:
    f.write(html_report)

print("Informe HTML generado con éxito.")

# Configurar pdfkit con la ruta a wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Convertir el informe HTML a PDF
try:
    pdfkit.from_file('informe.html', 'informe.pdf', configuration=config)
    print("Informe PDF generado con éxito.")
except OSError as e:
    print("Error al generar el informe PDF:", e)

# Convertir el informe HTML a Word
doc = Document()
with open('informe.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
    doc.add_paragraph(html_content)
doc.save('informe.docx')
print("Informe Word generado con éxito.")
