const preguntas = {
    "I. Calidad del Líder": [
        "El líder confirmó con el equipo los estándares de calidad acordes con los requerimientos del docente para el desarrollo del trabajo.",
        "El líder fue competente en su rol llevando las agendas de las reuniones presenciales con el equipo durante el desarrollo del proyecto."
    ],
    "II. Manejo de la comunicación": [
        "Al comunicarse con el equipo, explicó las ideas y los conceptos de manera que todos pudieran entender para lograr los resultados del proyecto.",
        "Facilitó la comunicación de los miembros de su equipo a través de las citaciones a reuniones y conversaciones presenciales y virtuales (chat).",
        "Comunicó la emoción y entusiasmo adecuados que motivaron a los miembros del equipo."
    ],
    "III. Ética profesional": [
        "Aceptó la responsabilidad de su rol y las decisiones que tomó y fue consciente del impacto que ellas tuvieron en los demás.",
        "Fue un modelo de rol que poseía como miembro del equipo y se puso como ejemplo apropiado para que los demás miembros del equipo lo siguieran.",
        "Fue abierto, honrado y franco en el trato con los miembros de su equipo."
    ],
    "IV. Planificación de trabajo": [
        "Fue eficiente en el desarrollo de los cursos de acción, en la programación de actividades y fue organizado.",
        "Estableció prioridades y metas claras.",
        "Fue flexible, y capaz de manejar la incertidumbre y evitó la frustración cuando las cosas no salían como se esperaba.",
        "Se aseguró de que los miembros de su equipo asumieran las responsabilidades que definieron cuando era apropiado."
    ],
    "V. Uso de sistemas apropiados": [
        "Supo organizar la información para que fluyera eficazmente para todos los miembros del equipo.",
        "Supo usar técnicas analíticas para resolver problemas o para llegar a conclusiones.",
        "Ayudó a identificar aspectos a mejorar para la entrega adecuada del proyecto."
    ],
    "VI. Toma de decisiones": [
        "Se comprometió con las decisiones que tomó y asumió responsabilidad de lo que hizo y no hizo.",
        "Respetó las decisiones de los miembros del equipo cuando fue apropiado.",
        "Desarrolló soluciones creativas e imaginativas cuándo enfrentó problemas poco familiares."
    ],
    "VII. Supervisión y seguimiento": [
        "El seguimiento de las responsabilidades de los miembros del equipo fue adecuado al tiempo para realizar el proyecto."
    ],
    "VIII. Ambiente de colaboración del equipo": [
        "Sus acciones contribuyeron a generar un ambiente saludable en el equipo de trabajo.",
        "Se aseguró de que los miembros recibieran el crédito por sus contribuciones y logros, cuando era apropiado.",
        "Aceptó los posibles errores como una parte normal del aprendizaje."
    ]
};

document.addEventListener('DOMContentLoaded', function () {
    const contenedorPreguntas = document.getElementById('preguntas');
    let contadorGobal = 1;

    for (const categoria in preguntas) {
        const preguntasCategoria = preguntas[categoria];

        //Título categoría
        const tituloCategoria = document.createElement('p');
        tituloCategoria.classList.add('habilidades')
        tituloCategoria.textContent = categoria;
        contenedorPreguntas.appendChild(tituloCategoria);

        //contenedor categoría
        const contenedorCategoria = document.createElement('div');
        contenedorCategoria.classList.add('cont_categoria');
        contenedorPreguntas.appendChild(contenedorCategoria);

        //Recorrer cada pregunta
        preguntasCategoria.forEach((pregunta) => {
            //crear la cadena con la etiqueta p y clase pregunta
            const textoPregunta = document.createElement('p');
            textoPregunta.classList.add('pregunta');
            textoPregunta.textContent = `${contadorGobal}. ${pregunta}`;

            //agrega la pregunta al contenedor de categoría
            contenedorCategoria.appendChild(textoPregunta);
            contadorGobal++;
        });
    }
});
