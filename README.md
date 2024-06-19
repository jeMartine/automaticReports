# Generador de Informes de Evaluación de Liderazgo

Este proyecto permite generar informes en formato PDF y Word a partir de datos de evaluación de liderazgo almacenados en archivos de Excel. Los informes incluyen gráficos de evaluación y respuestas a preguntas específicas sobre el desempeño del líder.

## Requisitos Previos

- Python 3.x
- Pandas
- NumPy
- Matplotlib
- Jinja2
- pdfkit
- docx
- pdf2docx

Además, necesitas tener instalado `wkhtmltopdf`. Puedes descargarlo desde [aquí](https://wkhtmltopdf.org/downloads.html).

## Instalación

1. Clona este repositorio en tu máquina local:
    ```bash
    git clone https://github.com/jeMartine/automaticReports.git
    ```

2. Instala las dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```

3. Configura la ruta de `wkhtmltopdf` en tu sistema y actualiza la variable `path_wkhtmltopdf` en el código con la ruta correcta.

## Uso

Para generar los informes, coloca tus archivos de Excel en la carpeta `respuestas`. Luego, ejecuta el siguiente comando:

```bash
python informe.py nombreArchivo.xlsx
```

Para generar informes para todos los archivos en la carpeta respuestas, utiliza:

```bash
python informe.py -all
```

# Descripción del Código
## Funciones Principales

- `capitalizar_palabras(cadena)`: Pone en mayúscula la primera letra de cada palabra de una cadena.
- `crear_grafico(df, preguntas, titulo, lider, cont_preguntas)`: Crea gráficos de barras para las evaluaciones y los guarda como archivos PNG.
- `leerExcel(nombreArchivo)`: Lee los datos de evaluación desde un archivo de Excel y organiza la información necesaria para generar los informes.
- `generarPDFs(df, graficos, datos, rutaSalida, mp, promedios)`: Genera archivos PDF y Word a partir de plantillas HTML usando los datos de evaluación y los gráficos.
- `deleteTemp()`: Elimina la carpeta temporal utilizada para almacenar archivos intermedios.
- `carpetaSalida(curso, mp)`: Crea las carpetas necesarias para almacenar los informes generados.
- `crearArchivoExcelPromedios(promedios, rutaSalida, cursoGen, mp, numeroClase)`: Crea un archivo Excel que resume los promedios de evaluación.
- `archivosCarpeta()`: Obtiene una lista de todos los archivos en la carpeta respuestas.
- `informesPorExcel(entrada)`: Función principal que coordina la generación de informes para un archivo de Excel específico.

## Ejecución del Script
El script se ejecuta desde la línea de comandos. Si no se proporcionan argumentos suficientes, se muestra un mensaje recordando el uso correcto.

## Estructura del Proyecto
- informe.py: Script principal para generar informes.
- vista/index.html: Plantilla HTML para los informes.
- respuestas/: Carpeta para almacenar los archivos de Excel con los datos de evaluación.
- vista/temp/: Carpeta temporal para archivos intermedios.
- salida/: Carpeta para almacenar los informes generados.
- imagenes/: Carpeta para las imágenes utilizadas en los informes.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

## Licencia
Este proyecto está bajo la Licencia MIT.
