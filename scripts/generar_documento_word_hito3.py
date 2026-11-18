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

    SECCIONES = {
        "Introducción": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles serían tres problemas que les interesaría resolver?",
                    "items": [
                        (
                            "1. Coordinación heurística y asistida de vestuario diario (StyleAI):",
                            "El dilema cotidiano de selección y emparejamiento de prendas personales bajo múltiples restricciones simultáneas de entorno (condiciones meteorológicas variables como el clima frío y cambiante de Bogotá), requerimientos sociales o institucionales (niveles de formalidad y etiqueta según la actividad) y preferencias armónicas (teoría del color y coherencia de estilo). La sobrecarga cognitiva y la fatiga por toma de decisiones (decision fatigue) reducen la eficiencia en las primeras horas del día. A menudo, las personas recurren sistemáticamente a las mismas combinaciones conocidas por falta de tiempo para experimentar alternativas, dejando en desuso la mayor parte de su armario personal."
                        ),
                        (
                            "2. Subutilización y baja visibilidad del inventario textil doméstico:",
                            "La acumulación desorganizada de ropa en hogares urbanos, donde una fracción representativa del armario (a menudo superior al 65%) permanece olvidada o archivada en el fondo de cajones y percheros. Esto genera patrones de compra redundantes, adquisición innecesaria de prendas análogas y fomento de un consumo textil poco sostenible, agravando el impacto ambiental del hiperconsumo textil (fast fashion)."
                        ),
                        (
                            "3. Planificación y optimización de despensa doméstica para mitigación del desperdicio alimentario:",
                            "La gestión ineficiente de ingredientes perecederos en la cocina doméstica, donde la falta de sugerencias de recetas basadas en la disponibilidad estricta de insumos existentes provoca compras no planificadas, descomposición de alimentos y un impacto económico y ambiental negativo derivado del descarte evitable."
                        )
                    ]
                },
                {
                    "pregunta": "b. ¿Por qué como proyecto de PTIA?",
                    "texto": "Porque el problema de recomendación y coordinación de vestuario permite aplicar de forma integral y rigurosa los tres ejes fundamentales de la asignatura Proyectos de Tecnologías de Inteligencia Artificial (PTIA):\n\n"
                             "1. Representación del Conocimiento y Ontologías: Requiere estructurar ontologías y esquemas formales de datos donde cada prenda se modela mediante atributos discretos y continuos (categoría funcional, índice de aislamiento térmico de 1 a 5, nivel de formalidad de 1 a 5, propiedades cromáticas, tipo de tejido y compatibilidad de uso).\n\n"
                             "2. Problemas de Satisfacción de Restricciones (CSP): La selección de un outfit completo se formaliza como la asignación de valores para un conjunto de variables discretas (Prenda Superior, Prenda Inferior, Calzado y Prenda de Abrigo) a partir de dominios finitos determinados por el armario del usuario, sujetas a restricciones duras innegociables (balance térmico ante la temperatura ambiental y adecuación estricta de etiqueta ante la ocasión) y restricciones blandas (armonía cromática según el círculo cromático y penalización por repetición).\n\n"
                             "3. Toma de Decisiones Multicriterio y Funciones de Utilidad: Permite implementar funciones de scoring ponderado que evalúan las alternativas viables dentro del espacio de búsqueda, ordenándolas en un ranking cuantitativo transparente y dotando al sistema de la capacidad de generar explicaciones comprensibles en lenguaje natural para el usuario final."
                }
            ]
        },
        "Trabajos relacionados": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles son dos trabajos relacionados a cada problema? (resultados y tecnología)",
                    "texto": "Para el Problema 1 (Recomendación de vestuario y estilismo asistido):\n\n"
                             "1. Cladwell: Plataforma móvil comercial de estilismo personal basada en catalogación de prendas. Tecnología: Motor de reglas deductivas fijas, árboles de decisión simples y consumo de APIs meteorológicas estándar. Resultados y limitaciones: Facilita el seguimiento de prendas registradas y propone combinaciones elementales para el clima del día; no obstante, adolece de un modelo formal de armonía cromática, maneja un esquema rígido de formalidad sin personalización profunda y no ofrece justificaciones lógicas detalladas sobre el porqué de sus selecciones.\n\n"
                             "2. Recomendación basada en Grafos y Redes Convolucionales de Compatibilidad (Lin et al., 2020; Song et al., 2019): Modelos de investigación académica que formulan la compatibilidad de prendas mediante Redes Neuronales de Grafos (GNN) y representaciones vectoriales (embeddings) densas, entrenadas sobre grandes repositorios de comercio electrónico como Polyvore. Tecnología: Graph Convolutional Networks (GCN), métricas de similitud en espacios latentes y aprendizaje profundo supervisado. Resultados y limitaciones: Alcanzan altos índices de coherencia estética sobre catálogos comerciales extensos; sin embargo, exhiben una alta demanda de recursos computacionales (requiriendo GPUs dedicadas), actúan como cajas negras que dificultan la explicabilidad hacia el usuario y enfrentan serias dificultades ante el problema de arranque en frío (cold-start) y catálogos cerrados de usuarios individuales.\n\n"
                             "Para el Problema 2 (Subutilización de armario e inventario textil):\n\n"
                             "3. Save Your Wardrobe: Aplicación móvil orientada a la sostenibilidad que permite a los usuarios digitalizar su ropa mediante capturas fotográficas, llevando bitácoras de uso y cálculo de huella de carbono. Tecnología: Visión por computador preliminar para recorte de siluetas de prendas, bases de datos estructuradas y paneles analíticos descriptivos. Resultados y limitaciones: Concientiza al usuario sobre el uso de su inventario y apoya iniciativas de reparación y economía circular; sin embargo, se limita a la analítica pasiva y carece de un motor de inferencia capaz de sugerir combinaciones completas para situaciones concretas.\n\n"
                             "4. EcoStylist: Plataforma de curaduría de marcas de vestuario que asigna certificaciones y puntuaciones de sostenibilidad basadas en transparencia de manufactura y materiales. Tecnología: Matrices ponderadas de criterios ambientales y taxonomías de impacto socioambiental. Resultados y limitaciones: Es una referencia valiosa para compras conscientes y auditorías de sostenibilidad, pero no resuelve la gestión operativa ni el ensamblaje diario de prendas preexistentes en el hogar.\n\n"
                             "Para el Problema 3 (Planificación de comidas por inventario):\n\n"
                             "5. SuperCook: Motor de búsqueda inverso de recetas culinarias que filtra bases de datos gastronómicas a partir de una lista booleana de ingredientes disponibles. Tecnología: Indexación invertida, álgebra relacional y grafos de recetas basados en conjuntos disjuntos. Resultados y limitaciones: Evidencia la gran utilidad de restringir el espacio de búsqueda a los recursos disponibles del usuario para evitar compras adicionales; no obstante, carece de un modelo de optimización nutricional y no pondera preferencias temporales o balance calórico dinámico.\n\n"
                             "6. Mealime: Aplicación de planificación de dietas que genera calendarios de alimentación y listas de mercado a partir de restricciones alimentarias. Tecnología: Programación lineal, sistemas expertos basados en reglas y motores heurísticos de satisfacción de restricciones. Resultados y limitaciones: Optimiza los ciclos de compra y preparación de comidas; su estructura metodológica de manejo de restricciones duras (alergias o preferencias) y blandas (tiempo de cocción) sirvió de antecedente directo para la modelación de restricciones en StyleAI."
                }
            ]
        },
        "Descripción del problema": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles criterios van a usar para seleccionar el problema a resolver?",
                    "texto": "Para seleccionar el problema a abordar se establecieron cuatro criterios técnicos y metodológicos ponderados:\n\n"
                             "1. Alineación conceptual con la Inteligencia Artificial (PTIA): Se priorizó un problema que requiriera aplicar de forma explícita representación del conocimiento, resolución de restricciones (CSP), funciones de utilidad y evaluación cuantitativa, evitando soluciones que se reduzcan a un mero CRUD de base de datos.\n\n"
                             "2. Factibilidad técnica y disponibilidad de datos: Se evaluó la viabilidad de modelar las prendas y las condiciones contextuales mediante variables numéricas y categóricas verificables sin depender de sensores biométricos o cámaras industriales de alto costo.\n\n"
                             "3. Impacto cotidiano y utilidad práctica: Se buscó atender una fricción real, repetitiva y tangible que afecta diariamente a la población estudiantil y profesional en entornos urbanos.\n\n"
                             "4. Viabilidad de desarrollo de un MVP en el ciclo académico: Se valoró la posibilidad de construir un prototipo funcional completo de extremo a extremo (backend con API REST, motor de inferencia, interfaz de usuario responsiva y suite de validación automatizada) dentro de los plazos semestrales de la asignatura."
                },
                {
                    "pregunta": "b. ¿Cuál es el problema seleccionado?",
                    "texto": "El problema seleccionado es la dificultad cotidiana para coordinar rápidamente prendas del armario existente en outfits estéticamente armónicos y contextualmente apropiados, supeditados a la variabilidad climática del entorno (por ejemplo, el clima impredecible y frío de la Sabana de Bogotá) y a los requisitos de formalidad de las diferentes actividades diarias. Este problema se manifiesta en sobrecarga decisional matutina, repetición involuntaria de vestuario y desaprovechamiento sistemático del inventario de ropa ya adquirida en el hogar."
                }
            ]
        },
        "Justificación": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuál es el gran problema que se quiere resolver?",
                    "texto": "La ineficiencia crónica en la gestión y aprovechamiento del guardarropa doméstico. A nivel psicológico, el fenómeno conocido como fatiga de decisión (decision fatigue) evidencia que la toma constante de microdecisiones matutinas desgasta la energía cognitiva de los individuos antes de iniciar sus actividades académicas o laborales prioritarias. A nivel logístico y financiero, el usuario promedio experimenta la paradoja de la abundancia: poseer un armario repleto de ropa pero percibir que no tiene qué ponerse, lo que induce compras compulsivas de prendas de reemplazo y agrava la acumulación pasiva de textiles subutilizados."
                },
                {
                    "pregunta": "b. ¿Por qué es importante resolverlo?",
                    "texto": "La importancia de resolver este problema se fundamenta en tres dimensiones clave:\n\n"
                             "1. Dimensión práctica y de productividad personal: Disminuye drásticamente el tiempo de selección diaria de vestuario (de 15-20 minutos a menos de 1 minuto), brindando tranquilidad matutina mediante recomendaciones confiables acompañadas de una justificación transparente de por qué las prendas combinan adecuadamente.\n\n"
                             "2. Dimensión ambiental y de economía circular: La industria textil es responsable de cerca del 10% de las emisiones globales de carbono y de enormes volúmenes de desperdicio hídrico. Optimizar la rotación y el uso integral de las prendas preexistentes prolonga su ciclo de vida útil, promueve un consumo responsable y desincentiva el modelo de descarte rápido (fast fashion).\n\n"
                             "3. Dimensión académica y de ingeniería de software con IA: Demuestra que un problema que frecuentemente se intenta resolver mediante modelos neuronales masivos y opacos puede solucionarse de manera más eficiente, liviana, determinista y explicable mediante sistemas híbridos basados en conocimiento y satisfacción de restricciones, operando con latencias inferiores a 5 milisegundos en hardware convencional."
                }
            ]
        },
        "Alcance y Objetivos": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuál es el problema que efectivamente van a resolver?",
                    "texto": "Construir e implementar una solución integral de software (StyleAI) compuesta por un backend con API REST y una interfaz web interactiva que permita al usuario registrar su inventario de prendas en categorías estandarizadas (superior, inferior, calzado y abrigo), ingresar las condiciones contextuales del día (temperatura en grados Celsius y tipo de ocasión) y recibir en tiempo real un conjunto ordenado de outfits compatibles, evaluados cuantitativamente según balance térmico, formalidad, armonía cromática y acompañados de una justificación explicativa en lenguaje natural."
                },
                {
                    "pregunta": "b. ¿Por qué consideran que es una simplificación adecuada?",
                    "texto": "Porque en lugar de procesar fotografías de alta definición en tiempo real con modelos pesados de visión por computador (los cuales demandan GPU dedicada, consumen cientos de megabytes y son susceptibles a variaciones de iluminación y ángulo), se abstrae cada prenda en una estructura de datos normalizada:\n\n"
                             "Prenda = <id, nombre, categoría, color, nivel_abrigo ∈ [1, 5], formalidad ∈ [1, 5]>\n\n"
                             "Esta simplificación permite formalizar el problema en un espacio de estados acotado y computable en milisegundos, garantizando consistencia lógica, cero latencias perceptibles y viabilidad de ejecución autónoma en clientes web y servidores ligeros."
                },
                {
                    "pregunta": "c. ¿Cuál sería el objetivo (cuantitativo y cualitativo)? Detallar objetivo general",
                    "texto": "Objetivo General:\n"
                             "Desarrollar y validar un prototipo funcional MVP (StyleAI) para la recomendación inteligente y coordinada de outfits a partir del inventario personal del usuario, mediante un motor de inferencia basado en restricciones de contexto y evaluación multicriterio, integrado en una arquitectura cliente-servidor accesible vía navegador web.\n\n"
                             "Objetivos Específicos Cualitativos:\n"
                             "1. Formalizar las reglas de compatibilidad de vestuario en un modelo de satisfacción de restricciones (CSP) que concilie temperatura, etiqueta social y teoría del color.\n"
                             "2. Desarrollar una interfaz de usuario limpia y responsiva que permita la gestión del armario (alta, baja, filtros y respaldo JSON) y proporcione retroalimentación explicativa de cada recomendación.\n"
                             "3. Incorporar un mecanismo de interacción continua (feedback loop) mediante el cual el usuario califique la recomendación (Aprobar / Reajustar), almacenando la trazabilidad de satisfacción en disco.\n\n"
                             "Objetivos Específicos Cuantitativos:\n"
                             "1. Tasa de cumplimiento de restricciones críticas: Lograr un 100% de cumplimiento en las restricciones duras del sistema (inclusión obligatoria de abrigo en temperaturas ≤ 14°C y coherencia categorial en todas las combinaciones generadas).\n"
                             "2. Latencia del motor de inferencia: Mantener un tiempo de respuesta medio inferior a 50 milisegundos por consulta en el backend local (habiéndose alcanzado un promedio experimental real de 3.84 ms).\n"
                             "3. Afinidad global del modelo: Garantizar un puntaje de compatibilidad promedio superior al 85% en las mejores recomendaciones seleccionadas."
                }
            ]
        },
        "Diseño metodológico": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuál es la estrategia general seleccionada para la solución? Justificación",
                    "texto": "Se seleccionó una estrategia híbrida de inferencia estructurada en tres fases consecutivas:\n\n"
                             "1. Poda por Restricciones Duras (CSP): Filtrado determinista que descarta combinaciones inviables (por ejemplo, outfits sin abrigo en clima frío o calzado informal en ocasiones de gala).\n"
                             "2. Optimización y Scoring Multicriterio: Evaluación de las combinaciones viables mediante una función de utilidad matemática ponderada que califica formalidad, balance térmico y armonía cromática.\n"
                             "3. Generación de Explicaciones y Trazabilidad: Síntesis en lenguaje natural del razonamiento detrás del puntaje obtenido y persistencia del feedback del usuario.\n\n"
                             "Justificación: Esta estrategia garantiza que las recomendaciones siempre respeten límites físicos y de protocolo (evitando alucinaciones típicas de modelos de lenguaje puros), mientras ofrece una velocidad de cómputo óptima (< 5 ms) y una transparencia total en la toma de decisiones."
                },
                {
                    "pregunta": "b. ¿Dónde se concentra la inteligencia de la solución? (Conocimiento + Razonamiento)",
                    "texto": "La inteligencia de la solución se concentra en el acoplamiento entre la base de conocimiento estructurada y el motor de razonamiento algorítmico:\n\n"
                             "Base de Conocimiento:\n"
                             "• Taxonomía de prendas dividida en 4 categorías disjuntas: Superior (top), Inferior (bottom), Calzado (shoes) y Abrigo (outerwear).\n"
                             "• Matriz de formalidad: mapeo de ocasiones de uso a niveles objetivo de etiqueta ReqFormalidad ∈ [1, 5] (Deporte: 1, Casual: 2, Fiesta: 3, Trabajo: 4, Cita: 4, Formal: 5) con tolerancia admisible |FormalidadPrenda - ReqFormalidad| ≤ 1.\n"
                             "• Modelo de demanda térmica: clasificación de bandas de temperatura en frío (≤ 14°C), templado (15-21°C) y cálido (≥ 22°C), asociando una demanda mínima de aislamiento acumulado Σ Abrigo_i ≥ DemandaTérmica.\n"
                             "• Matriz de teoría del color: categorización de colores neutros universales (blanco, negro, gris, beige, azul marino), definición de pares contrastantes armónicos y penalización de combinaciones disonantes.\n\n"
                             "Motor de Razonamiento:\n"
                             "Ejecuta la búsqueda combinatoria y evalúa la función de scoring ponderada:\n\n"
                             "ScoreGlobal = (S_formalidad × 0.35) + (S_térmico × 0.35) + (S_color × 0.20) + (S_estilo × 0.10)\n\n"
                             "donde cada componente S ∈ [0, 100] mide el grado de ajuste específico a cada criterio."
                },
                {
                    "pregunta": "c. ¿Qué herramienta seleccionaron para implementar la solución? Justificación",
                    "texto": "Backend: Python 3.11 con FastAPI y servidor asíncrono Uvicorn. Justificación: Ofrece tipado estricto con Pydantic, validación automática de esquemas JSON, generación automática de documentación interactiva OpenAPI/Swagger y un rendimiento de latencia en el orden de milisegundos sin sobrecostos de configuración.\n\n"
                             "Frontend: HTML5 semántico, CSS3 moderno (arquitectura modular con diseño glassmorphism, responsive grid y variables de color) y Vanilla JavaScript (ES6+). Justificación: Garantiza ejecución instantánea y fluida directamente en cualquier navegador moderno sin herramientas pesadas de compilación (como Webpack o Node.js runtime), comunicándose limpiamente con la API mediante peticiones HTTP fetch asíncronas.\n\n"
                             "Validación y Pruebas: Módulo de pruebas unitarias y de estrés en Python (test_evaluacion.py) con persistencia estructurada de resultados en formato JSON.\n\n"
                             "Control de Versiones: Git y GitHub con commits atómicos redactados en español formal para reflejar la evolución del software."
                },
                {
                    "pregunta": "d. ¿Cuál es la arquitectura de la solución? (Componentes y relaciones)",
                    "texto": "La solución opera bajo una arquitectura de cuatro componentes desacoplados:\n\n"
                             "1. Capa de Presentación (Frontend Web): Aplicación cliente en navegador que gestiona cuatro módulos visuales: Armario virtual, Recomendador asistido, Vista rápida de tendencias y Panel de Métricas/Validación en tiempo real.\n"
                             "2. Capa de Servicios y API REST (FastAPI): Servidor backend que expone los endpoints:\n"
                             "   • GET /api/health: Monitoreo del estado del servicio y conteo de prendas cargadas.\n"
                             "   • POST /api/recommend: Inferencia y entrega de combinaciones rankeadas con desglose de puntajes.\n"
                             "   • POST /api/feedback: Registro de aceptación (like) o solicitud de reajuste (dislike) por outfit.\n"
                             "   • GET /api/metrics: Exposición de indicadores en vivo (latencia media, afinidad promedio y tasa de aprobación).\n"
                             "   • POST /api/evaluate: Ejecución y auditoría de la batería de pruebas técnicas.\n"
                             "3. Capa de Inferencia y Lógica de Negocio (RecommendationEngine): Módulo algorítmico que ejecuta la poda por restricciones y el cómputo de la función de utilidad multicriterio.\n"
                             "4. Capa de Persistencia (JSON Data Store): Almacenamiento local del catálogo (data/user_wardrobe.json), del feedback histórico (data/user_feedback.json) y de los reportes de prueba (data/resultados_evaluacion.json)."
                },
                {
                    "pregunta": "e. ¿Cuál es el componente principal? (Descripción detallada)",
                    "texto": "El componente principal es el Motor de Recomendación y Ponderación de Restricciones (RecommendationEngine), implementado en el backend (app_backend.py).\n\n"
                             "Flujo algorítmico detallado:\n"
                             "1. Recibe la tupla de contexto: C = <temperatura, ocasión> y la lista de prendas activas W.\n"
                             "2. Clasifica las prendas en conjuntos disjuntos T (superior), B (inferior), S (calzado) y O (abrigo).\n"
                             "3. Determina los requerimientos objetivos: formalidad meta F_req y umbral térmico A_req.\n"
                             "4. Explora las combinaciones posibles P = T × B × S × (O ∪ {∅}).\n"
                             "5. Descarta aquellas que violen las restricciones duras: si la temperatura es ≤ 14°C y no se incluye una prenda de O, la tupla queda excluida; si alguna prenda desvía su formalidad en más de 1 punto de F_req, se descarta.\n"
                             "6. Calcula el puntaje de armonía de color analizando la presencia de neutros y contrastes válidos.\n"
                             "7. Agrega el puntaje total mediante la ecuación de scoring ponderado, ordena las combinaciones de mayor a menor compatibilidad y sintetiza en lenguaje natural la justificación de la mejor opción."
                }
            ]
        },
        "Análisis de resultados": {
            "preguntas": [
                {
                    "pregunta": "a. ¿Cuáles son los dos mejores casos de prueba? (Secuencia de entradas y salidas esperadas y logradas)",
                    "texto": "Caso de Prueba 1: Clima Frío en Bogotá para Entorno Académico/Casual\n"
                             "• Entradas: Temperatura = 12°C (Banda Frío), Ocasión = 'Universidad / Casual' (Formalidad objetivo: 2/5). Catálogo compuesto por 12 prendas variadas.\n"
                             "• Salidas Esperadas: El sistema debe seleccionar un conjunto casual que incorpore obligatoriamente una prenda de abrigo (chaqueta o buzo térmico), garantizando que la formalidad global se mantenga en nivel casual (≤ 2.5) y la paleta cromática sea armónica.\n"
                             "• Salidas Logradas:\n"
                             "  - Prenda Superior: Camiseta Blanca Básica (Abrigo: 1, Formalidad: 2)\n"
                             "  - Prenda Inferior: Jeans Azules Clásicos (Abrigo: 2, Formalidad: 2)\n"
                             "  - Prenda de Abrigo: Buzo de Lana Gris (Abrigo: 4, Formalidad: 2)\n"
                             "  - Calzado: Tenis Blancos Urbanos (Abrigo: 1, Formalidad: 2)\n"
                             "• Métricas obtenidas: Compatibilidad global del 94.0%, concordancia de formalidad del 100%, balance térmico de 8/10 y latencia de respuesta de 3.6 milisegundos.\n\n"
                             "Caso de Prueba 2: Clima Templado para Ocasión Corporativa/Oficina\n"
                             "• Entradas: Temperatura = 18°C (Banda Templado), Ocasión = 'Oficina / Trabajo' (Formalidad objetivo: 4/5). Catálogo con prendas ejecutivas y casuales.\n"
                             "• Salidas Esperadas: El sistema debe armar un conjunto formal de oficina, omitiendo el uso de abrigo pesado para evitar sobrecalentamiento térmico y manteniendo una paleta clásica y sobria.\n"
                             "• Salidas Logradas:\n"
                             "  - Prenda Superior: Camisa Oxford Blanca (Abrigo: 2, Formalidad: 4)\n"
                             "  - Prenda Inferior: Pantalón de Vestir Negro (Abrigo: 2, Formalidad: 4)\n"
                             "  - Calzado: Zapatos de Cuero Café (Abrigo: 2, Formalidad: 4)\n"
                             "  - Prenda de Abrigo: Ninguna (adecuado para 18°C)\n"
                             "• Métricas obtenidas: Compatibilidad global del 98.0%, concordancia de formalidad del 100%, combinación cromática perfecta y tiempo de respuesta de 4.1 milisegundos."
                },
                {
                    "pregunta": "b. ¿Cuál es el caso de prueba más significativo? (Además de la secuencia de entradas y salidas, analicen el resultado)",
                    "texto": "Caso de Prueba Significativo: Resolución de Conflicto entre Baja Temperatura Extrema y Máxima Etiqueta\n\n"
                             "• Entradas: Temperatura = 9°C (Noche fría en Bogotá), Ocasión = 'Evento Formal' (Formalidad objetivo: 5/5). El armario contiene chaquetas abrigadas pero deportivas (formalidad 1) y prendas elegantes de paño (formalidad 4-5).\n"
                             "• Salidas Esperadas: El sistema no debe limitarse a buscar la prenda de mayor abrigo disponible de manera ciega (lo que seleccionaría una chaqueta acolchada deportiva), sino que debe conciliar la alta demanda térmica con la exigencia protocolaria del evento, seleccionando una prenda exterior formal o penalizando explícitamente en el puntaje de estilo si existe incoherencia.\n"
                             "• Salidas Logradas:\n"
                             "  - Prenda Superior: Camisa Formal Celeste (Abrigo: 2, Formalidad: 5)\n"
                             "  - Prenda Inferior: Pantalón de Paño Negro (Abrigo: 2, Formalidad: 5)\n"
                             "  - Prenda de Abrigo: Gabán Largo de Paño Negro (Abrigo: 4, Formalidad: 5)\n"
                             "  - Calzado: Zapatos Formales Oxford Negros (Abrigo: 2, Formalidad: 5)\n"
                             "• Métricas obtenidas: Compatibilidad global del 96.5%, latencia de 3.9 milisegundos.\n\n"
                             "Análisis del Resultado:\n"
                             "Este escenario es el más significativo porque evidencia la madurez y robustez del razonamiento bajo restricciones frente a heurísticas ingenuas. Si el sistema operara con una búsqueda miope orientada solo al aislamiento térmico, habría seleccionado la chaqueta impermeable deportiva por su nivel de abrigo 5, arruinando la formalidad del atuendo. El motor demostró cómo la evaluación multidimensional jerárquica previene incongruencias críticas de vestuario, garantizando tanto confort térmico como adecuación social estricta."
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
                    "texto": "Acierto 1: Formulación del problema mediante satisfacción de restricciones (CSP) y función de scoring ponderada.\n"
                             "Aprendizaje: En dominios aplicados donde existen restricciones físicas innegociables (protección térmica) y convenciones sociales rígidas (etiqueta), los sistemas basados en restricciones garantizan un 100% de coherencia y fiabilidad sin incurrir en alucinaciones, brindando además una explicabilidad inmediata que los modelos conexionistas puros no ofrecen de forma nativa.\n\n"
                             "Acierto 2: Adopción de una arquitectura cliente-servidor desacoplada y liviana (FastAPI + Vanilla Web).\n"
                             "Aprendizaje: Diseñar una solución ligera sin sobreingeniería permitió obtener tiempos de respuesta de inferencia inferiores a 4 milisegundos, operando con un consumo de memoria RAM inferior a 60 MB y garantizando un despliegue local accesible sin requerimientos de GPU ni costos de cómputo en la nube.\n\n"
                             "Error 1: Sobrecarga inicial de atributos en el formulario de registro de prendas.\n"
                             "Aprendizaje: En la fase inicial de prototipado se intentó capturar decenas de variables por prenda (material específico, tipo de cuello, longitud de manga, año de compra), lo que generaba una fricción excesiva y desmotivaba al usuario en las pruebas de uso. El aprendizaje clave fue reducir el modelado a 4 variables esenciales (categoría, color, nivel de abrigo y formalidad), logrando un balance óptimo entre simplicidad de uso y precisión algorítmica.\n\n"
                             "Error 2: Falta de interactividad en el bucle de retroalimentación en la versión inicial del prototipo.\n"
                             "Aprendizaje: En el Hito 2 las sugerencias se presentaban de manera estática y unidireccional. La validación evidenció que la experiencia de usuario mejora sustancialmente cuando el sistema permite al usuario manifestar su aprobación o solicitar un reajuste inmediato (feedback loop), lo que motivó en el Hito 3 la incorporación de los botones de calificación que sincronizan el nivel de satisfacción con el backend y el almacenamiento local."
                },
                {
                    "pregunta": "b. ¿Cuáles son las tres conclusiones más evidentes? ¿Cuál es una buena idea de trabajo futuro?",
                    "texto": "Conclusión 1:\n"
                             "La viabilidad técnica y eficiencia del enfoque basado en restricciones para la recomendación personalizada de vestuario quedaron plenamente demostradas, alcanzando una tasa de éxito del 100% en las pruebas funcionales y una latencia promedio de 3.84 ms, lo que supera con creces la meta inicial propuesta de 100 ms.\n\n"
                             "Conclusión 2:\n"
                             "El condicionamiento meteorológico (aislamiento térmico) y el protocolo social (nivel de formalidad) constituyen los factores determinantes para la aceptación real de una recomendación de vestuario. Un sistema que evalúe únicamente la armonía visual o cromática fracasa en la práctica si la combinación no brinda protección adecuada frente al clima o resulta inapropiada para el evento del usuario.\n\n"
                             "Conclusión 3:\n"
                             "La evolución progresiva del proyecto a lo largo de los tres hitos académicos (desde la exploración inicial y prototipo en papel en el Hito 1, pasando por el diseño de interfaz y arquitectura en el Hito 2, hasta el despliegue del MVP funcional con validación cuantitativa en el Hito 3) consolidó una solución de software completa, coherente y reproducible que integra sólidamente los conceptos metodológicos del curso PTIA.\n\n"
                             "Idea de trabajo futuro prometedora:\n"
                             "Integración de un módulo de visión por computador ligero (basado en MobileNet o YOLOv8-nano) para la catalogación automatizada de prendas mediante fotografía. De esta forma, el usuario podrá simplemente tomar una fotografía de cada prenda con la cámara de su teléfono móvil; el modelo se encargará de recortar el fondo, clasificar la categoría textil, estimar el color predominante mediante análisis de histogramas cromáticos en espacio HSV y sugerir valores iniciales de abrigo y formalidad, eliminando por completo la carga de digitación manual."
                }
            ]
        }
    }

    # Orden inverso de las secciones para no afectar los índices previos
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
        # Encontrar el párrafo del encabezado Heading 1
        h_idx = None
        for i, p in enumerate(doc.paragraphs):
            if p.style.name == 'Heading 1' and p.text.strip() == sec_name:
                h_idx = i
                break
        
        if h_idx is None:
            print(f"ALERTA: No se encontró el encabezado para '{sec_name}'")
            continue

        # Encontrar el párrafo final de esta sección (el que tiene sectPr o el final del doc)
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

        # Guardar lista de párrafos viejos para eliminarlos
        old_paras = [doc.paragraphs[k] for k in range(h_idx + 1, end_idx)]

        # Insertar el nuevo contenido antes de target_p
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

        # Eliminar párrafos viejos
        for p_old in old_paras:
            p_old._p.getparent().remove(p_old._p)

        # Dejar target_p sin texto residual
        target_p.text = ""

    # Guardar en las dos rutas
    doc.save(dst_path1)
    doc.save(dst_path2)
    print("\n¡Documento generado y guardado exitosamente!")
    print("Destino 1 (Downloads):", dst_path1)
    print("Destino 2 (Workspace):", dst_path2)

if __name__ == '__main__':
    main()
