import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from jinja2 import Environment, FileSystemLoader 
import pdfkit


# Configurar la ruta de wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Actualiza esta ruta según tu instalación
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

options = {
    'enable-local-file-access': None,  # Necesario para que wkhtmltopdf pueda acceder a archivos locales
    'page-size': 'letter',
    'encoding': 'UTF-8',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'no-outline': None
}

# Pone en mayuscula la primera letra de cada palabra
def capitalizar_palabras(cadena):
    return cadena.title()

#Carpeta para almacenar los gráficos
if not os.path.exists('vista/graficos'):
    os.makedirs('vista/graficos')

#1. leer excel
#2. agrupar por lider las evaluaciones
#3. crear las gráficas
#4. cargar el html
#5. exportar html a pdf y word 

def crear_grafico(df, preguntas, titulo, lider, cont_preguntas):

    # Agrupar por el nombre del líder
    grupos_lider = df.groupby("Seleccione el nombre de Líder a evaluar.")
    grupo = grupos_lider.get_group(lider)
    labelEstudiante= ['Estudiante 1', 'Estudiante 2']

    
    estudiantes = grupo['Escriba su nombre completo'].tolist()
    evaluaciones = {estudiante: grupo.loc[grupo['Escriba su nombre completo'] == estudiante, preguntas].values.flatten().tolist() for estudiante in estudiantes}

    x = np.arange(len(preguntas))  # Posiciones en el eje X para las preguntas
    width = 0.2  # Ancho de las barras

    fig, ax = plt.subplots()

    # Crear las barras para cada estudiante
    for i, estudiante in enumerate(estudiantes):
        evals = evaluaciones[estudiante]
        ax.bar(x + i * width, evals, width, label=labelEstudiante[i])

    # Configurar etiquetas y título
    #ax.set_title(titulo)
    ax.set_xticks(x + width * (len(estudiantes) - 1) / 2)
    ax.set_xticklabels([f'Pregunta {p + cont_preguntas}' for p in range(len(preguntas))])
    ax.set_ylim(0, 5)  # Establecer los límites del eje y de 0 a 5
    ax.legend()

    plt.tight_layout()
    #plt.show()

    nombre_archivo = f'vista/graficos/{lider}_{titulo}.png'.replace(" ", "_").replace(",","")
    nombre_archivo_toPDF = f'graficos/{lider}_{titulo}.png'.replace(" ", "_").replace(",","")
    plt.savefig(nombre_archivo)
    plt.close()
    return nombre_archivo_toPDF


def leerExcel(nombreArchivo):
    #leer el archivo de excel
    try:
        print("Leyendo excel")
        df= pd.read_excel(nombreArchivo)
       
        # Definir las preguntas por grupo
        grupos_preguntas = {
            'Grupo 1': [
                '1. El líder confirmó con el equipo los estándares de calidad acordes con los requerimientos del docente para el desarrollo del trabajo.',
                '2. El líder fue competente en su rol haciendo seguimiento de la diligencia del kanban por parte de los integrantes del equipo y las agendas de las reuniones virtuales con el equipo durante el desarrollo del proyecto.',
            ],
            'Grupo 2': [
                '3. Al comunicarse con el equipo, enfocó las ideas y los conceptos de manera que todos pudieran entender para lograr los resultados del proyecto.',
                '4. Facilitó la comunicación de los miembros de su equipo a través de las citaciones a reuniones y conversaciones virtuales (chat)',
                '5. Comunicó emoción y entusiasmo adecuados que motivaron a los miembros del equipo.'
            ],
            'Grupo 3': [
                '6. Aceptó la responsabilidad de su rol y las decisiones que tomó y fue consciente del impacto que ellas tuvieron en los demás.',
                '7. Fue un modelo de rol que poseía como miembro del equipo  y se puso como ejemplo apropiado para que los demás miembros del equipo lo siguieran.',
                '8. Fue abierto, honrado y franco en el trato con los miembros de su equipo.'
            ],
            'Grupo 4': [
                '9. Fue eficiente en el desarrollo de los cursos de acción, en la programación de actividades y fue organizado.',
                '10. Estableció prioridades y metas claras.',
                '11. Fue flexible, y capaz de manejar la incertidumbre y evitó la frustración cuando las cosas no salían como se esperaba ',
                '12. Se aseguró de que los miembros de su equipo asumieran las responsabilidades que definieron.'
            ],
            'Grupo 5': [
                '13. Supo organizar la información para que  fluyera eficazmente para todos los miembros del equipo.',
                '14. Supo usar técnicas analíticas para resolver problemas o para llegar a conclusiones ',
                '15. Ayudó a identificar aspectos a mejorar para la entrega adecuada del proyecto '
            ],
            'Grupo 6': [
                '16. Se comprometió con las decisiones que tomó y asumió responsabilidad de lo que hizo y no hizo .',
                '17. Respetó  las decisiones de los miembros del equipo cuando fue apropiado ',
                '18. Desarrolló soluciones creativas e imaginativas cuándo enfrentó problemas poco familiares.'
            ],
            'Grupo 7': [
                '19.El seguimiento de las responsabilidades de los miembros  del equipo fue adecuada al tiempo para realizar el proyecto.'
            ],
            'Grupo 8': [
                '20. Sus acciones contribuyeron a generar un ambiente saludable en el equipo de trabajo.',
                '21. Se aseguró de que los miembros recibieran el crédito por sus contribuciones y logros, cuando era apropiado.',
                '22. Aceptó los posibles errores como una parte normal del aprendizaje.'
            ]
        }
    
        lideres = df["Seleccione el nombre de Líder a evaluar."].unique()

        graficos = {lider: {} for lider in lideres}
        for lider in lideres:
            cont_preguntas=1
            print(f'Graficos {lider}')
            for grupo, preguntas in grupos_preguntas.items():
                titulo = f'{grupo}'
                nombre_archivo = crear_grafico(df, preguntas, titulo, lider, cont_preguntas)
                graficos[lider][grupo]=nombre_archivo
                cont_preguntas += len(preguntas)
        
        return df, graficos

    except FileNotFoundError:
        print("No se encontró el archivo especificado")
    except Exception as e:
        print("Ocurrió un error al leer el archivo", str(e))

def generarPDFs(df, graficos, datos):
    # Cargar la plantilla HTML usando Jinja2
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('vista/index.html')

    lideres = df["Seleccione el nombre de Líder a evaluar."].unique()

    for lider in lideres:
        # Filtrar la información de los estudiantes para el líder actual
        grupo_lider = df[df["Seleccione el nombre de Líder a evaluar."] == lider]
        estudiantes = grupo_lider['Escriba su nombre completo'].tolist()

        # Columnas de texto
        estilo_liderazgo = grupo_lider['De acuerdo con los estilos de liderazgo de la Tabla anterior, ¿Cuál o cuáles considera fue el de su líder.(señale con una x una o varias opciones)'].tolist()
        razon_estilo = grupo_lider['¿Por qué considera que su líder cumple con los Estilos de Liderazgo que usted escogió en la pregunta anterior? (sí contestó NINGUNO, por favor explique)'].tolist()
        trabajaria_otro = grupo_lider['¿Trabajaría bajo su liderazgo en otra oportunidad?'].tolist()
        razon_trabajaria = grupo_lider['¿Por qué?'].tolist()

         # Crear lógica para las respuestas de "¿Trabajaría bajo su liderazgo en otra oportunidad?"
        trabajarOtro1Si = "SI" if len(trabajaria_otro) > 0 and trabajaria_otro[0] == "SI" else ""
        trabajarOtro1No = "NO" if len(trabajaria_otro) > 0 and trabajaria_otro[0] == "NO" else ""
        trabajarOtro2Si = "SI" if len(trabajaria_otro) > 1 and trabajaria_otro[1] == "SI" else ""
        trabajarOtro2No = "NO" if len(trabajaria_otro) > 1 and trabajaria_otro[1] == "NO" else ""

        # Rellenar la plantilla con los datos específicos de cada líder
        html_content = template.render(
            numSemestre=datos["numSemestre"],
            ahno=datos["ahno"],
            clase=datos["clase"],
            estudiante1=estudiantes[0] if len(estudiantes) > 0 else "",
            estudiante2=estudiantes[1] if len(estudiantes) > 1 else "",
            lider=capitalizar_palabras(lider),
            grafico1=graficos[lider]['Grupo 1'],
            grafico2=graficos[lider]['Grupo 2'],
            grafico3=graficos[lider]['Grupo 3'],
            grafico4=graficos[lider]['Grupo 4'],
            grafico5=graficos[lider]['Grupo 5'],
            grafico6=graficos[lider]['Grupo 6'],
            grafico7=graficos[lider]['Grupo 7'],
            grafico8=graficos[lider]['Grupo 8'],
            res1Estudiante1=estilo_liderazgo[0] if len(estilo_liderazgo) > 0 else "",  
            res1Estudiante2=estilo_liderazgo[1] if len(estilo_liderazgo) > 1 else "",
            res2Estudiante1=razon_estilo[0] if len(razon_estilo) > 0 else "",
            res2Estudiante2=razon_estilo[1] if len(razon_estilo) > 1 else "",
            trabajarOtro1Si=trabajarOtro1Si,
            trabajarOtro1No=trabajarOtro1No,
            trabajarOtro2Si=trabajarOtro2Si,
            trabajarOtro2No=trabajarOtro2No,
            res3Estudiante1=razon_trabajaria[0] if len(razon_trabajaria) > 0 else "",
            res3Estudiante2=razon_trabajaria[1] if len(razon_trabajaria) > 1 else "",
            defLider=""  # Agregar la calificación final real del líder
        )

        lider = capitalizar_palabras(lider)

        # Guardar el contenido HTML en un archivo temporal
        with open(f'vista/temp_{lider}.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
            print(f'Creado vista/temp_{lider}.html')

        ruta_leer = f'vista/temp_{lider}.html'
        # Convertir el archivo HTML a PDF
        pdfkit.from_file(ruta_leer, output_path=f'Informe_{lider}.pdf', configuration=config, options=options)
        print(f'Generado: Informe_{lider}.pdf')


if __name__ == "__main__":
    # ruta_html = 'vista/index.html'
    # ruta_css = 'vista/style.css'
    datos = {
        "numSemestre": "Segundo", 
        "ahno": "2024", 
        "clase": "Electrónica"
    }
    
    if len(sys.argv)<2:
        print("Recuerde: python informe.py nombreArchivo.xlsx")
    else:
        nombre_excel = "respuestas/" + sys.argv[1]
        df, graficos = leerExcel(nombre_excel)
        generarPDFs(df, graficos, datos)