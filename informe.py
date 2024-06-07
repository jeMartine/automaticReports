import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    ax.set_title(titulo)
    ax.set_xticks(x + width * (len(estudiantes) - 1) / 2)
    ax.set_xticklabels([f'Pregunta {p + cont_preguntas}' for p in range(len(preguntas))])
    ax.set_ylim(0, 5)  # Establecer los límites del eje y de 0 a 5
    ax.legend()

    plt.tight_layout()
    plt.show()


def leerExcel(nombreArchivo):
    #leer el archivo de excel
    try:
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

        for lider in lideres:
            cont_preguntas=1
            for grupo, preguntas in grupos_preguntas.items():
                titulo = f'Evaluaciones del Líder {lider} - {grupo}'
                crear_grafico(df, preguntas, titulo, lider, cont_preguntas)
                cont_preguntas += len(preguntas)

    except FileNotFoundError:
        print("No se encontró el archivo especificado")
    except Exception as e:
        print("Ocurrió un error al leer el archivo", str(e))



if __name__ == "__main__":
    ruta_html = 'vista/index.html'
    ruta_css = 'vista/style.css'
    datos = {
        "numSemestre": "Segundo", 
        "ahno": "2024", 
        "clase": "Electrónica", 
        "estudiante1": "Jorge Martinez", 
        "estudiante2": "otra persona", 
        "lider": "GONZALEZ CARRILLO JOSE GUILLERMO ANTONIO DE JESUS"
    }
    ruta_salida = 'prueba2.pdf'

    if len(sys.argv)<2:
        print("Recuerde: python informe.py nombreArchivo.xlsx")
    else:
        leerExcel(sys.argv[1])