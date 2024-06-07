import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#1. leer excel
#2. agrupar por lider las evaluaciones
#3. crear las gráficas
#4. cargar el html
#5. exportar html a pdf y word 

def leerExcel(nombreArchivo):
    #leer el archivo de excel
    try:
        df= pd.read_excel(nombreArchivo)
        # columnas_seleccionadas = df.iloc[:, 2:7]
        # print(columnas_seleccionadas)

        #agrupar por el nombre del lider
        #se agrupa por la columna de lider
        grupos_lider= df.groupby("Seleccione el nombre de Líder a evaluar.")

        #iterar en cada grupo
        for lider, grupo in grupos_lider:
            #muestra el lider
            print(f"Líder: {lider}\n")
            
            estudiantes = grupo['Escriba su nombre completo']
            preguntas = ['Pregunta 1', 'Pregunta 2', 'Pregunta 3', 'Pregunta 4']
            labelEstudiante= ['Estudiante 1', 'Estudiante 2']

            evaluaciones = {estudiante: grupo.loc[grupo['Escriba su nombre completo'] == estudiante, ['1. El líder confirmó con el equipo los estándares de calidad acordes con los requerimientos del docente para el desarrollo del trabajo.',
                                                                                                  '2. El líder fue competente en su rol haciendo seguimiento de la diligencia del kanban por parte de los integrantes del equipo y las agendas de las reuniones virtuales con el equipo durante el desarrollo del proyecto.']].values.flatten().tolist() for estudiante in estudiantes}

            x = np.arange(len(preguntas))
            width = 0.2

            fig, ax = plt.subplots()

            #barras de cada estudiante
            for i, estudiante in enumerate(estudiantes):
                evals = evaluaciones[estudiante]
                ax.bar(x+i * width, evals, width, label=labelEstudiante[i])

            # Configurar etiquetas y título
            ax.set_xticks(x + width * (len(estudiantes) - 1) / 2)
            ax.set_xticklabels(preguntas)
            ax.set_ylim(0,5)
            ax.legend()

            plt.tight_layout()
            plt.show()


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