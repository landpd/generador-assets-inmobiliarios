Actúa como un experto Desarrollador Frontend y Diseñador UI con Tailwind CSS. Vamos a crear una nueva plantilla de carrusel inmobiliario y a integrarla en el sistema.
Fase 1: Absorción de Contexto (¡OBLIGATORIO LEER PRIMERO!)
Antes de escribir código, utiliza tus herramientas para leer el contenido exacto de:
manual_reglas_visuales_propiedades.txt (Para entender la paleta estricta, la regla de contraste y la prohibición de uppercase en EB Garamond).
biblioteca_recursos.txt y recursos_graficos.py (Para saber cómo inyectar SVGs como el logo o íconos, y si hay texturas útiles).
plantillas_carruseles_inmobiliarias.py (Para ver cómo están estructuradas las funciones actuales, como disenio_landscape_5fotos, y cómo extraen las variables del diccionario datos).
4. Librerías de UI (Opcional pero recomendado): Utiliza componentes de código abierto gratuitos como HyperUI, Flowbite, Preline o Aceternity UI como inspiración estructural para evitar codificar layouts desde cero.
Fase 2: Creación de la Nueva Plantilla
En el archivo plantillas_carruseles_inmobiliarias.py, crea una nueva función llamada disenio_[NOMBRE_DEL_ESTILO]_5fotos(datos).
Esta plantilla debe constar exactamente de 5 slides en un contenedor flex-row de 5400x1350px.
Brief de Diseño para esta plantilla:
[ AQUÍ DESCRIBES TU IDEA. Ej: "Quiero un estilo 'Dark Mode Premium'. El fondo general debe ser #212322. Usa letras blancas. En el slide 2 y 4 pon las fotos en forma de círculos. En el slide 5, el botón debe ser amarillo con texto blanco." ]
Asegúrate de extraer las variables img1 a img5, calle, colonia_estado, precio, atributos_html, tipo_operacion y logo exactamente igual que en las otras funciones.

REGLAS INQUEBRANTABLES DE DISEÑO:
- Numeración de Slides: Si incluyes un indicador numérico (ej. '01/05'), la portada NO se cuenta. El primer slide de contenido (donde el índice del bucle for es i=1) debe imprimir '01'. Usa la fórmula str(i).zfill(2) en lugar de i+1.
- Tipografía EB Garamond: Queda estrictamente prohibido usar uppercase (all caps). Además, DEBES aplicar SIEMPRE un interlineado holgado como leading-[1.1] o leading-tight para evitar que las letras choquen verticalmente.
Fase 3: Integración en la Interfaz (Streamlit)
Abre pages/2_Automatizacion_Metricool.py.
Busca el diccionario PLANTILLAS_DISPONIBLES en la parte superior.
Añade la nueva función al diccionario con un nombre clave, por ejemplo:
"Arquetipo D: [Nombre de tu Estilo]": plantillas_carruseles_inmobiliarias.disenio_[NOMBRE_DEL_ESTILO]_5fotos
Nota: No necesitas modificar la lógica de rotación del Paso 6, ya que el sistema calcula dinámicamente el módulo (i % len(lista_plantillas)) basándose en el tamaño de este diccionario.
Ejecuta estos 3 pasos, guarda los archivos y avísame para previsualizar la nueva plantilla.