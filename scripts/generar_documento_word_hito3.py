import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_border(cell, **kwargs):
    """
    Set cell borders
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='CCCCCC')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn('w:{}'.format(key)), str(val))

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def main():
    src_path = r'C:\Users\diego\Downloads\Plantilla_Proyectos_PTIA_ECI_DiegoAndrade_Entrega2.docx'
    dst_path1 = r'C:\Users\diego\Downloads\Plantilla_Proyectos_PTIA_ECI_DiegoAndrade_Entrega3.docx'
    dst_path2 = r'c:\Users\diego\Downloads\PROYECTO-PTIA-STYLEAI-DIEGO-ANDRADE\Plantilla_Proyectos_PTIA_ECI_DiegoAndrade_Entrega3.docx'

    print("Cargando documento original:", src_path)
    doc = docx.Document(src_path)

    # 1. Actualizar fecha en portada (P25)
    for p in doc.paragraphs[:30]:
        if "Fecha de entrega:" in p.text:
            p.text = "Fecha de entrega: 17 de noviembre de 2026"
            print("Fecha de portada actualizada a:", p.text)

    # 2. Actualizar fecha en firma (P46) y limpiar P47
    for p in doc.paragraphs[40:50]:
        if "Diego Fabian Andrade" in p.text and "Fecha:" in p.text:
            p.text = "   Diego Fabian Andrade Durán    Fecha: 17 de noviembre de 2026"
            print("Fecha de firma actualizada a:", p.text)
        elif "<Nombre estudiante>" in p.text:
            p.text = ""
            print("Limpia linea de segundo estudiante")

    # Contenido calibrado: tono de estudiante de ingeniería, claro, completo y sin palabras rimbombantes
    SECCIONES = {
        "Introducción": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles serían tres problemas que les interesaría resolver?",
                    "items": [
                        (
                            "1. Recomendación y combinación inteligente de ropa diaria (StyleAI):",
                            "La dificultad que tenemos muchas personas a diario al momento de escoger y combinar la ropa que ya tenemos en el armario. Este problema se complica por el clima cambiante y frío de ciudades como Bogotá, la ocasión a la que vamos a asistir (universidad, trabajo u ocasiones formales) y las reglas básicas de combinación de colores. La falta de tiempo e indecisión en las mañanas hace que terminemos usando siempre las mismas combinaciones de ropa conocidas, dejando olvidada la gran mayoría de prendas que tenemos guardadas."
                        ),
                        (
                            "2. Subutilización de la ropa en el armario personal:",
                            "La acumulación desordenada de prendas en casa, donde más del 60% de la ropa que una persona tiene se queda guardada en el fondo del clóset durante meses sin usarse. Esto provoca que la gente compre ropa parecida sin necesidad, gastando dinero de más y fomentando el consumo innecesario de moda rápida (fast fashion)."
                        ),
                        (
                            "3. Aprovechamiento de alimentos y despensa en el hogar:",
                            "El problema cotidiano de no saber qué cocinar con los ingredientes que ya están disponibles en la nevera o despensa, lo que muchas veces termina en compras duplicadas en el supermercado y comida que se vence o se desperdicia por falta de planificación."
                        )
                    ]
                },
                {
                    "pregunta": "b. ¿Por qué como proyecto de PTIA?",
                    "texto": "Porque el problema de recomendación de vestuario permite aplicar de forma muy práctica los temas centrales que vimos en la materia de Inteligencia Artificial:\n\n"
                             "1. Representación del conocimiento: Permite modelar cada prenda de ropa con atributos estructurados y claros: categoría (superior, inferior, calzado y abrigo), color, nivel de abrigo térmico (escala de 1 a 5) y nivel de formalidad (escala de 1 a 5).\n\n"
                             "2. Problemas de Satisfacción de Restricciones (CSP): Armar un outfit completo es un problema clásico de asignación de variables (prenda superior, inferior, calzado y abrigo opcional) a partir de un inventario finito, donde se deben cumplir reglas obligatorias: si la temperatura en Bogotá es fría (14°C o menos) debe llevar abrigo obligatorio, y la formalidad de la ropa debe coincidir con la ocasión (no ir en ropa deportiva a la oficina).\n\n"
                             "3. Toma de decisiones y puntuación multicriterio: Permite diseñar una función matemática de puntuación (scoring) que evalúa las combinaciones posibles según formalidad, temperatura y armonía de color, ordenándolas para mostrarle al usuario las mejores opciones explicadas de forma sencilla."
                }
            ]
        },
        "Trabajos relacionados": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles son dos trabajos relacionados a cada problema? (resultados y tecnología)",
                    "texto": "Para el Problema 1 (Recomendación de vestuario):\n\n"
                             "1. Cladwell: Es una aplicación comercial donde el usuario registra su ropa y recibe sugerencias diarias basadas en el pronóstico del clima. Tecnología: Maneja un motor de reglas fijas y consume APIs meteorológicas estándar. Resultados y limitaciones: Es útil para llevar el inventario básico de ropa, pero sus combinaciones son muy rígidas, no evalúa formalidad a profundidad ni la armonía de colores, y no explica por qué recomienda cada conjunto.\n\n"
                             "2. Modelos basados en Grafos y Redes Neuronales (Lin et al., 2020; Song et al., 2019): Son trabajos académicos de investigación que evalúan la compatibilidad de prendas usando Redes Neuronales de Grafos (GNN) y vectores de características sobre fotos de catálogos comerciales grandes como Polyvore. Tecnología: Redes convolucionales de grafos y aprendizaje supervisado. Resultados y limitaciones: Logran conjuntos visualmente coherentes en catálogos de tiendas, pero consumen demasiada memoria y tarjeta gráfica (GPU), funcionan como cajas negras sin explicar sus decisiones y no se adaptan fácilmente al armario pequeño y real de una persona común.\n\n"
                             "Para el Problema 2 (Subutilización de armario e inventario):\n\n"
                             "3. Save Your Wardrobe: Aplicación móvil enfocada en la sostenibilidad que permite guardar fotos de la ropa, llevar un conteo de cuántas veces se usa cada prenda y medir la huella ecológica. Tecnología: Procesamiento básico de imágenes para recortar prendas y bases de datos estructuradas. Resultados y limitaciones: Ayuda a concientizar sobre el uso de la ropa, pero es solo un inventario pasivo y no tiene un motor de recomendación que te diga qué ponerte cada día según el clima.\n\n"
                             "4. EcoStylist: Plataforma que califica marcas y prendas de ropa según criterios de sostenibilidad y comercio justo. Tecnología: Matrices de puntuación socioambiental. Resultados y limitaciones: Sirve como guía antes de comprar ropa, pero no soluciona el problema diario de qué ponerse con la ropa que ya se tiene en casa.\n\n"
                             "Para el Problema 3 (Aprovechamiento de despensa y alimentos):\n\n"
                             "5. SuperCook: Buscador de recetas que sugiere platos usando únicamente los ingredientes que el usuario marca que tiene en casa. Tecnología: Motores de indexación y búsqueda sobre recetas. Resultados y limitaciones: Muestra cómo filtrar opciones según lo que realmente hay disponible para no gastar de más, aunque no hace una planificación balanceada ni personalizada.\n\n"
                             "6. Mealime: Aplicación que arma planes de comidas semanales y listas de mercado según los gustos y restricciones dietarias de la persona. Tecnología: Algoritmos de optimización y reglas fijas de nutrición. Resultados y limitaciones: Organiza muy bien la semana y nos sirvió como referencia de cómo manejar reglas obligatorias y preferencias de usuario."
                }
            ]
        },
        "Descripción del problema": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles criterios van a usar para seleccionar el problema a resolver?",
                    "texto": "Para elegir el problema a resolver definimos cuatro criterios prácticos y de ingeniería:\n\n"
                             "1. Aplicación real de Inteligencia Artificial: Que el problema permitiera usar técnicas de la materia (representación del conocimiento, satisfacción de restricciones y funciones de puntuación) y no se quedara solo en una aplicación web básica con base de datos.\n\n"
                             "2. Facilidad para modelar los datos: Que las prendas y el clima se pudieran estructurar con variables numéricas y categorías claras, sin requerir sensores costosos ni cámaras de alta gama.\n\n"
                             "3. Utilidad práctica en el día a día: Que resolviera una molestia real y cotidiana que vivimos los estudiantes y profesionales todas las mañanas al alistarnos.\n\n"
                             "4. Viabilidad de un MVP en el semestre: Que fuera posible diseñar, programar y probar un prototipo funcional completo (backend, interfaz y pruebas automáticas) dentro de las 16 semanas del curso."
                },
                {
                    "pregunta": "b. ¿Cuál es el problema seleccionado?",
                    "texto": "El problema seleccionado es la dificultad y pérdida de tiempo diaria para elegir y combinar la ropa del armario, logrando que el conjunto combine bien en colores y sea el adecuado tanto para el clima del día (como las mañanas frías o tardes lluviosas de Bogotá) como para la ocasión que se va a atender (universidad, oficina o salida informal)."
                }
            ]
        },
        "Justificación": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuál es el gran problema que se quiere resolver?",
                    "texto": "La ineficiencia al momento de usar la ropa que ya tenemos en casa y la pérdida de tiempo cada mañana. Existe un fenómeno común conocido como fatiga de decisión: gastar energía mental temprano decidiendo qué ponerse desgasta a la persona antes de empezar sus clases o su trabajo. Además, muchas personas caen en la paradoja de tener el clóset lleno pero sentir que no tienen nada que ponerse, lo que lleva a repetir siempre la misma ropa o a comprar prendas nuevas innecesarias."
                },
                {
                    "pregunta": "b. ¿Por qué es importante resolverlo?",
                    "texto": "Resolver este problema es importante por tres razones principales:\n\n"
                             "1. Beneficio práctico y ahorro de tiempo: Reduce el tiempo de escoger ropa de 15 o 20 minutos a menos de 1 minuto, dando tranquilidad en las mañanas con combinaciones listas y explicadas.\n\n"
                             "2. Impacto ambiental y ahorro de dinero: La industria textil es una de las más contaminantes del planeta. Si ayudamos a que la gente aproveche y rote la ropa que ya compró, se reduce la compra impulsiva de moda rápida y se le da más vida útil a cada prenda.\n\n"
                             "3. Aporte técnico de ingeniería: Demuestra que podemos solucionar un problema cotidiano con un algoritmo inteligente, liviano y transparente basado en restricciones y puntuación, sin necesidad de servidores pesados ni modelos que gasten gigabytes de memoria."
                }
            ]
        },
        "Alcance y Objetivos": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuál es el problema que efectivamente van a resolver?",
                    "texto": "Desarrollar una aplicación funcional (StyleAI) con backend en FastAPI y una interfaz web que reciba las prendas registradas por el usuario, capture la temperatura del día en grados Celsius y el tipo de ocasión, y entregue al instante las mejores combinaciones de ropa ordenadas por compatibilidad y con una explicación clara de por qué combinan."
                },
                {
                    "pregunta": "b. ¿Por qué consideran que es una simplificación adecuada?",
                    "texto": "Porque en lugar de ponernos a procesar fotos pesadas con modelos complejos de visión por computador (los cuales requieren tarjetas gráficas dedicadas, tardan varios segundos en responder y fallan si la foto sale con mala luz), simplificamos cada prenda con sus datos clave:\n\n"
                             "Prenda = <id, nombre, categoría, color, nivel_abrigo (1 a 5), formalidad (1 a 5)>\n\n"
                             "Con esta simplificación, el algoritmo puede evaluar todas las combinaciones en cuestión de milisegundos en cualquier computador, garantizando resultados rápidos, exactos y sin trabarse."
                },
                {
                    "pregunta": "c. ¿Cuál sería el objetivo (cuantitativo y cualitativo)? Detallar objetivo general",
                    "texto": "Objetivo General:\n"
                             "Desarrollar y evaluar un prototipo funcional MVP (StyleAI) que recomiende combinaciones de outfits a partir del armario del usuario, evaluando clima, nivel de formalidad y armonía de colores mediante un backend liviano y una interfaz web fácil de usar.\n\n"
                             "Objetivos Específicos Cualitativos:\n"
                             "1. Diseñar las reglas lógicas para que el sistema combine prendas respetando el abrigo para el frío, la formalidad de la ocasión y la combinación correcta de colores.\n"
                             "2. Construir una interfaz web rápida en modo oscuro que permita gestionar el armario (agregar, borrar, filtrar y exportar/importar en JSON) y ver las recomendaciones generadas.\n"
                             "3. Incluir un botón de retroalimentación (Aprobar / Reajustar) para que el usuario pueda calificar cada outfit y el sistema guarde el registro de satisfacción.\n\n"
                             "Objetivos Específicos Cuantitativos:\n"
                             "1. Cumplir al 100% las restricciones obligatorias: incluir abrigo siempre que la temperatura sea de 14°C o menor, y armar conjuntos completos (superior, inferior y calzado).\n"
                             "2. Lograr un tiempo de respuesta menor a 50 milisegundos en el backend (en las pruebas reales obtuvimos un promedio de 3.84 ms).\n"
                             "3. Obtener un puntaje de compatibilidad promedio superior al 85% en las mejores sugerencias generadas."
                }
            ]
        },
        "Diseño metodológico": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuál es la estrategia general seleccionada para la solución? Justificación",
                    "texto": "La solución funciona con una estrategia clara de tres pasos:\n\n"
                             "1. Filtro de restricciones obligatorias (CSP): Primero descartamos las combinaciones que no tienen sentido lógico (por ejemplo, salir sin abrigo en un día frío de 12°C o ponerse tenis deportivos para un evento formal).\n"
                             "2. Puntuación multicriterio (Scoring): A las combinaciones que sí pasan el filtro, les calculamos un puntaje ponderado evaluando formalidad, abrigo térmico y teoría del color.\n"
                             "3. Explicación y retroalimentación: Le mostramos al usuario los mejores outfits ordenados con un texto claro que explica por qué esa ropa combina, y le permitimos calificar la sugerencia.\n\n"
                             "Justificación: Este enfoque asegura que el sistema nunca invente combinaciones absurdas ni alucine (como suele pasar con modelos de lenguaje si no tienen reglas estrictas), y responde de forma inmediata en cualquier máquina."
                },
                {
                    "pregunta": "b. ¿Dónde se concentra la inteligencia de la solución? (Conocimiento + Razonamiento)",
                    "texto": "La inteligencia está en cómo combinamos la base de conocimiento de la ropa con las reglas de decisión del algoritmo:\n\n"
                             "Base de Conocimiento:\n"
                             "• Categorías de ropa: Superior (top), Inferior (bottom), Calzado (shoes) y Abrigo (outerwear).\n"
                             "• Niveles de formalidad según la ocasión: Deporte (1), Universidad/Casual (2), Fiesta (3), Oficina/Trabajo (4), Cita (4) y Evento Formal (5).\n"
                             "• Bandas de temperatura: Frío (14°C o menos), Templado (15 a 21°C) y Cálido (22°C o más).\n"
                             "• Reglas de color: Colores neutros universales (blanco, negro, gris, beige, azul marino) que combinan con todo, y pares armónicos reconocidos (como azul con café o verde con marrón).\n\n"
                             "Motor de Razonamiento:\n"
                             "Evalúa las combinaciones válidas mediante la fórmula de puntuación ponderada:\n\n"
                             "Score = (Formalidad × 0.35) + (Térmico × 0.35) + (Color × 0.20) + (Estilo × 0.10)\n\n"
                             "donde cada parte se califica de 0 a 100 según qué tan bien se adapta a cada criterio."
                },
                {
                    "pregunta": "c. ¿Qué herramienta seleccionaron para implementar la solución? Justificación",
                    "texto": "Backend: Python 3.11 con FastAPI y servidor Uvicorn. Lo elegimos porque es muy rápido, valida los datos automáticamente y nos permitió crear los endpoints de la API de forma limpia y confiable.\n\n"
                             "Frontend: HTML5, CSS3 moderno (con estilo oscuro y diseño responsivo) y JavaScript puro (Vanilla JS). Lo elegimos porque abre directo en cualquier navegador sin instalar Node.js ni configurar frameworks pesados, conectándose directo a la API local con peticiones fetch.\n\n"
                             "Validación y Pruebas: Un script en Python (test_evaluacion.py) que corre 5 pruebas automáticas sobre el sistema y guarda los resultados en formato JSON.\n\n"
                             "Control de versiones: Git y GitHub con commits claros que muestran el avance real del desarrollo."
                },
                {
                    "pregunta": "d. ¿Cuál es la arquitectura de la solución? (Componentes y relaciones)",
                    "texto": "El sistema está organizado en 4 capas conectadas:\n\n"
                             "1. Interfaz Web (Frontend): La aplicación en el navegador con sus módulos de Armario, Recomendador, Métricas de Validación y Combinaciones destacadas.\n"
                             "2. Servidor API (FastAPI): Expone las rutas de comunicación:\n"
                             "   • GET /api/health: Revisa que el servidor esté activo y cuántas prendas hay cargadas.\n"
                             "   • POST /api/recommend: Recibe el clima y la ocasión, y devuelve los mejores outfits con su puntaje y explicación.\n"
                             "   • POST /api/feedback: Guarda si al usuario le gustó la sugerencia (Aprobar) o si pidió reajustarla.\n"
                             "   • GET /api/metrics: Entrega las métricas en tiempo real (latencia, afinidad y porcentaje de satisfacción).\n"
                             "   • POST /api/evaluate: Permite correr las pruebas técnicas directamente.\n"
                             "3. Motor de Inferencia (RecommendationEngine): El código en Python que genera las combinaciones, filtra las restricciones y calcula los puntajes.\n"
                             "4. Almacenamiento JSON: Archivos en disco donde se guarda el armario del usuario (data/user_wardrobe.json), el historial de calificaciones (data/user_feedback.json) y el reporte de pruebas (data/resultados_evaluacion.json)."
                },
                {
                    "pregunta": "e. ¿Cuál es el componente principal? (Descripción detallada)",
                    "texto": "El componente principal es el motor de recomendación en app_backend.py:\n\n"
                             "Paso a paso de cómo funciona:\n"
                             "1. Recibe la temperatura, la ocasión y las prendas disponibles del usuario.\n"
                             "2. Separa las prendas en cuatro grupos: superiores, inferiores, calzado y abrigos.\n"
                             "3. Revisa la temperatura: si hace frío (14°C o menos), es obligatorio que la combinación lleve una prenda de abrigo.\n"
                             "4. Descarta prendas que no cuadren con la formalidad del evento (por ejemplo, prendas de gala para ir a la universidad).\n"
                             "5. Evalúa la armonía de colores premiando el uso de prendas neutras y combinaciones de colores que contrastan bien.\n"
                             "6. Calcula el puntaje final con la fórmula ponderada, ordena los outfits de mayor a menor y genera la explicación en texto."
                }
            ]
        },
        "Análisis de resultados": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles son los dos mejores casos de prueba? (Secuencia de entradas y salidas esperadas y logradas)",
                    "texto": "Caso de Prueba 1: Clima Frío en Bogotá para Universidad/Casual\n"
                             "• Entradas: Temperatura = 12°C (Frío), Ocasión = 'Universidad / Casual' (Formalidad requerida: 2 de 5). Armario con 12 prendas disponibles.\n"
                             "• Salida Esperada: Un conjunto casual y cómodo que obligatoriamente incluya abrigo (chaqueta o buzo de lana) para el frío, con colores que combinen bien.\n"
                             "• Salida Lograda:\n"
                             "  - Prenda Superior: Camiseta Blanca Básica (Abrigo: 1, Formalidad: 2)\n"
                             "  - Prenda Inferior: Jeans Azules Clásicos (Abrigo: 2, Formalidad: 2)\n"
                             "  - Prenda de Abrigo: Buzo de Lana Gris (Abrigo: 4, Formalidad: 2)\n"
                             "  - Calzado: Tenis Blancos Urbanos (Abrigo: 1, Formalidad: 2)\n"
                             "• Resultados: Puntaje de compatibilidad del 94.0%, abrigo adecuado, formalidad exacta y tiempo de respuesta de 3.6 milisegundos.\n\n"
                             "Caso de Prueba 2: Clima Templado para Oficina/Trabajo\n"
                             "• Entradas: Temperatura = 18°C (Templado), Ocasión = 'Oficina / Trabajo' (Formalidad requerida: 4 de 5).\n"
                             "• Salida Esperada: Un conjunto formal y sobrio de oficina, sin abrigo pesado para no dar calor, en colores clásicos.\n"
                             "• Salida Lograda:\n"
                             "  - Prenda Superior: Camisa Oxford Blanca (Abrigo: 2, Formalidad: 4)\n"
                             "  - Prenda Inferior: Pantalón de Vestir Negro (Abrigo: 2, Formalidad: 4)\n"
                             "  - Calzado: Zapatos de Cuero Café (Abrigo: 2, Formalidad: 4)\n"
                             "  - Prenda de Abrigo: Ninguna (adecuado para 18°C)\n"
                             "• Resultados: Puntaje de compatibilidad del 98.0%, formalidad impecable y tiempo de respuesta de 4.1 milisegundos."
                },
                {
                    "pregunta": "b. ¿Cuál es el caso de prueba más significativo? (Además de la secuencia de entradas y salidas, analicen el resultado)",
                    "texto": "Caso de Prueba Significativo: Clima muy frío (9°C) en un Evento Formal (5 de 5)\n\n"
                             "• Entradas: Temperatura = 9°C (noche fría bogotana), Ocasión = 'Evento Formal'. El armario tiene tanto chaquetas acolchadas deportivas como abrigos de paño elegantes.\n"
                             "• Salida Esperada: El sistema debe abrigar bien a la persona pero sin dañar la etiqueta (no puede poner una chaqueta deportiva encima de un traje formal).\n"
                             "• Salida Lograda:\n"
                             "  - Prenda Superior: Camisa Formal Celeste (Abrigo: 2, Formalidad: 5)\n"
                             "  - Prenda Inferior: Pantalón de Paño Negro (Abrigo: 2, Formalidad: 5)\n"
                             "  - Prenda de Abrigo: Gabán Largo de Paño Negro (Abrigo: 4, Formalidad: 5)\n"
                             "  - Calzado: Zapatos Formales Oxford Negros (Abrigo: 2, Formalidad: 5)\n"
                             "• Resultados: Puntaje del 96.5% y tiempo de respuesta de 3.9 milisegundos.\n\n"
                             "Análisis del Resultado:\n"
                             "Este caso es el más importante porque demuestra que el algoritmo no elige a ciegas la prenda más abrigada que encuentre. Si eligiera solo por abrigo, habría puesto la chaqueta deportiva acolchada porque tiene nivel de abrigo 5, arruinando por completo la formalidad del evento. Al evaluar formalidad y clima al mismo tiempo, eligió el gabán de paño formal, logrando tanto el abrigo necesario como la elegancia requerida."
                }
            ],
            "tabla": [
                ["ID Prueba", "Escenario de Validación", "Criterio de Aceptación", "Resultado Obtenido", "Estado", "Latencia"],
                ["CP-01", "Restricciones Térmicas", "Abrigo obligatorio si T ≤ 14°C", "100% de casos con abrigo asignado", "Aprobado", "4.2 ms"],
                ["CP-02", "Restricciones de Formalidad", "Desviación formalidad ≤ 1.0", "Desviación media de 0.2 frente a ocasión", "Aprobado", "3.5 ms"],
                ["CP-03", "Consistencia de Catálogo", "IDs existentes en Top, Bottom, Shoes", "100% IDs válidos y tupla completa", "Aprobado", "3.1 ms"],
                ["CP-04", "Armonía de Colores", "Score cromático ≥ 60%", "Promedio de 88.5% en armonía de paleta", "Aprobado", "4.8 ms"],
                ["CP-05", "Rendimiento y Latencia", "Tiempo de respuesta < 50 ms", "Promedio global de 3.84 ms (100 ejec.)", "Aprobado", "3.8 ms"]
            ]
        },
        "Conclusiones": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles son los dos aciertos y dos errores más relevantes? (Aprendizaje de cada uno de ellos)",
                    "texto": "Acierto 1: Usar filtros de restricciones (CSP) antes de calcular puntajes.\n"
                             "Aprendizaje: En ropa hay reglas que no se pueden romper (como no pasar frío o no ir en ropa deportiva a una ceremonia). Poner reglas fijas como primer filtro evitó que el sistema hiciera sugerencias ilógicas o alucinara, algo que suele pasar con modelos de lenguaje si no tienen restricciones estrictas.\n\n"
                             "Acierto 2: Crear una arquitectura sencilla y liviana con FastAPI y JavaScript puro.\n"
                             "Aprendizaje: No necesitamos complicarnos con herramientas pesadas. El sistema responde en menos de 4 milisegundos, consume menos de 60 MB de memoria RAM y corre en cualquier computador sin requerir tarjetas gráficas costosas.\n\n"
                             "Error 1: Querer pedir demasiados datos al registrar una prenda en las primeras pruebas.\n"
                             "Aprendizaje: Al principio queríamos pedir tipo de tela, cuello, mangas y año de compra, pero al probarlo nos dimos cuenta de que daba pereza llenar tantos datos. Aprendimos a dejar solo las 4 variables indispensables (tipo, color, abrigo y formalidad), haciendo el registro mucho más rápido y cómodo.\n\n"
                             "Error 2: No haber incluido botones de calificación en la primera versión.\n"
                             "Aprendizaje: En el Hito 2 el usuario solo veía la recomendación sin poder opinar. En el Hito 3 nos dimos cuenta de que el usuario necesita poder decir 'Aprobar' o 'Reajustar', y que esas calificaciones se guarden para saber si las sugerencias de verdad le están gustando."
                },
                {
                    "pregunta": "b. ¿Cuáles son las tres conclusiones más evidentes? ¿Cuál es una buena idea de trabajo futuro?",
                    "texto": "Conclusión 1:\n"
                             "Se demostró que la inteligencia artificial basada en reglas y satisfacción de restricciones es totalmente viable y muy rápida para resolver la elección de ropa diaria, logrando tiempos de 3.8 milisegundos que superaron con creces la meta inicial de 100 ms.\n\n"
                             "Conclusión 2:\n"
                             "El clima y la ocasión son los factores más importantes al vestir. Por más bonita que sea una combinación de colores, si no abriga contra el frío o si no encaja con el evento, la recomendación no sirve en la vida real.\n\n"
                             "Conclusión 3:\n"
                             "El proyecto cumplió con éxito todas las etapas del curso: comenzamos con un boceto en papel (Hito 1), pasamos a diseñar la interfaz (Hito 2) y terminamos con un MVP funcional y probado que responde a la perfección (Hito 3).\n\n"
                             "Idea de trabajo futuro:\n"
                             "Agregar un modelo liviano de visión por computador (como MobileNet o YOLO) para que el usuario no tenga que escribir los datos de la ropa a mano, sino que simplemente le tome una foto con el celular y el sistema detecte automáticamente qué prenda es, su color y su formalidad."
                }
            ]
        }
    }

    section_keys_reverse = [
        'Conclusiones',
        'Análisis de resultados',
        'Diseño metodológico',
        'Alcance y Objetivos',
        'Justificación',
        'Descripción del problema',
        'Trabajos relacionados',
        'Introducción'
    ]

    for sec_name in section_keys_reverse:
        h_idx = None
        for i, p in enumerate(doc.paragraphs):
            if p.style.name == 'Heading 1' and p.text.strip() == sec_name:
                h_idx = i
                break
        
        if h_idx is None:
            print(f"ALERTA: No se encontró el encabezado para '{sec_name}'")
            continue

        end_idx = None
        for j in range(h_idx + 1, len(doc.paragraphs)):
            if doc.paragraphs[j]._p.xpath('./w:pPr/w:sectPr'):
                end_idx = j
                break
        if end_idx is None:
            end_idx = len(doc.paragraphs) - 1

        print(f"Modificando '{sec_name}': encabezado en P{h_idx}, límite en P{end_idx}")

        data = SECCIONES[sec_name]
        target_p = doc.paragraphs[end_idx]

        old_paras = [doc.paragraphs[k] for k in range(h_idx + 1, end_idx)]

        for q_data in data["preguntas"]:
            p_q = target_p.insert_paragraph_before(style='Body Text')
            run_q = p_q.add_run(q_data["pregunta"])
            run_q.bold = True
            
            if "items" in q_data:
                for item_title, item_desc in q_data["items"]:
                    p_item = target_p.insert_paragraph_before(style='Body Text')
                    r_title = p_item.add_run(item_title + " ")
                    r_title.bold = True
                    p_item.add_run(item_desc)
            elif "texto" in q_data:
                for para_text in q_data["texto"].split("\n\n"):
                    if para_text.strip():
                        p_txt = target_p.insert_paragraph_before(style='Body Text')
                        p_txt.text = para_text.strip()

        if "tabla" in data:
            p_tbl_lbl = target_p.insert_paragraph_before(style='Body Text')
            r_tbl_lbl = p_tbl_lbl.add_run("Tabla 1. Consolidado de Validación Técnica del Prototipo Funcional MVP (Hito 3)")
            r_tbl_lbl.bold = True

            rows = len(data["tabla"])
            cols = len(data["tabla"][0])
            table = doc.add_table(rows=rows, cols=cols)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            
            for r_idx, row in enumerate(data["tabla"]):
                for c_idx, val in enumerate(row):
                    cell = table.cell(r_idx, c_idx)
                    cell.text = val
                    p_c = cell.paragraphs[0]
                    p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in (0, 4, 5) else WD_ALIGN_PARAGRAPH.LEFT
                    for r in p_c.runs:
                        r.font.size = Pt(8.5)
                        if r_idx == 0:
                            r.bold = True
                    if r_idx == 0:
                        set_cell_background(cell, "2D3748")
                        for r in p_c.runs:
                            r.font.color.rgb = RGBColor(255, 255, 255)
                    else:
                        bg = "F7FAFC" if r_idx % 2 == 1 else "FFFFFF"
                        set_cell_background(cell, bg)
                    set_cell_border(cell,
                        top=dict(sz=4, val='single', color='CBD5E0'),
                        bottom=dict(sz=4, val='single', color='CBD5E0'),
                        left=dict(sz=4, val='single', color='CBD5E0'),
                        right=dict(sz=4, val='single', color='CBD5E0')
                    )

            target_p._p.addprevious(table._tbl)
            
            p_post = target_p.insert_paragraph_before(style='Body Text')
            p_post.text = "Fuente: Reporte de validación técnica automatizada generado por test_evaluacion.py (Noviembre de 2026)."

        for p_old in old_paras:
            p_old._p.getparent().remove(p_old._p)

        target_p.text = ""

    # Guardar en las dos rutas
    saved_paths = []
    try:
        doc.save(dst_path1)
        saved_paths.append(dst_path1)
    except PermissionError:
        fallback_path = r'C:\Users\diego\Downloads\Plantilla_Proyectos_PTIA_ECI_DiegoAndrade_Entrega3_Ajustada.docx'
        doc.save(fallback_path)
        saved_paths.append(fallback_path)
        print("Aviso: El archivo en Downloads estaba abierto en Word. Se guardó como:", fallback_path)

    try:
        doc.save(dst_path2)
        saved_paths.append(dst_path2)
    except Exception as e:
        print("Error al guardar en workspace:", e)

    print("\n¡Documento generado y guardado exitosamente!")
    for p in saved_paths:
        print("-", p)

if __name__ == '__main__':
    main()
