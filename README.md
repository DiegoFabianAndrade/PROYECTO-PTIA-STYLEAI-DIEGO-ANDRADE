# StyleAI — Recomendador de Outfits y Gestión de Armario Inteligente

> **Escuela Colombiana de Ingeniería Julio Garavito**  
> **Asignatura / Programa:** Proyecto de Inteligencia Artificial Aplicada (PTIA)  
> **Autor:** Diego Andrade  
> **Entrega Evaluada:** Hito 3 — Solución y Evaluación (3er Tercio - Semana 16)  
> **Estado del Prototipo:** Prototipo Funcional MVP v2.0 (Implementado y Validado)

---

## 📌 1. Descripción del Proyecto y Propósito

**StyleAI** es una solución de software inteligente orientada a reducir la fatiga de decisión diaria en la elección de vestuario. Integra un modelo de recomendación basado en compatibilidad contextual, una interfaz web interactiva y un servicio backend de inferencia que analiza de manera conjunta:
- **Restricciones térmicas:** Nivel de abrigo requerido según la temperatura y condición climática (frío, templado, cálido, lluvioso).
- **Restricciones de etiqueta y formalidad:** Nivel de formalidad exigido por el entorno u ocasión (universidad/casual, oficina/trabajo, fiesta/noche, evento formal/gala, deporte, cita).
- **Armonía cromática:** Reglas de contraste y combinación entre prendas superiores, inferiores, calzado y prendas exteriores (regla 60-30-10 y compatibilidad de tonos neutros).
- **Preferencia de estilo del usuario:** Filtrado de prendas según estilos definidos (casual, elegante, urbano, deportivo, minimalista).

---

## 🏗️ 2. Evolución del Prototipo: De Interfaz (Hito 2) a Funcional MVP (Hito 3)

Cumpliendo con la taxonomía de prototipos establecida en la rúbrica institucional de la asignatura, el proyecto ha completado su evolución:

| Nivel de Prototipo | Objetivo Principal | Características Implementadas en StyleAI |
| :--- | :--- | :--- |
| **Prototipo de Interfaz (Hito 2)** | Validar la experiencia de usuario (UX) e interacción inicial. | Interfaz navegable, maquetación con estilos de alto contraste, simulación visual de resultados y validación de componentes interactivos. |
| **Prototipo Funcional MVP (Hito 3)** | Demostrar viabilidad técnica real y validar la solución mediante pruebas estructuradas. | **Funcionalidades reales implementadas:** motor de recomendación ponderado, API backend funcional en FastAPI, validación automática de restricciones térmicas y de formalidad, gestión de catálogo con importación/exportación JSON, registro persistente de calificaciones de usuario (feedback) y panel de métricas en vivo. |

---

## 📁 3. Estructura de Fuentes del Diseño y del Código (Versión Final)

El repositorio organiza de forma modular las fuentes de diseño, código backend, suite de pruebas y datos del sistema:

```text
PROYECTO-PTIA-STYLEAI-DIEGO-ANDRADE/
├── styleai_app/                      # FUENTES DEL DISEÑO Y FRONTEND
│   ├── index.html                    # Maquetación HTML5 semántica y accesible
│   ├── style.css                     # Sistema visual, tokens de diseño y componentes
│   ├── app.js                        # Lógica de cliente, conexión API y suite en vivo
│   └── assets/                       # Iconografía y recursos gráficos
│       ├── logo.png                  # Identidad gráfica del sistema
│       ├── top.svg                   # Vector prenda superior
│       ├── bottom.svg                # Vector prenda inferior
│       ├── shoes.svg                 # Vector calzado
│       └── outerwear.svg             # Vector prenda exterior
├── data/                             # FUENTES DE DATOS Y REGISTROS
│   ├── styleai_dataset.jsonl         # Dataset sintético estructurado (500 muestras)
│   ├── resultados_evaluacion.json    # Resultados exportados de la suite de pruebas
│   └── user_feedback.json            # Calificaciones y retroalimentación de usuarios
├── app_backend.py                    # Servidor API backend en FastAPI (v2.0.0-mvp)
├── test_evaluacion.py                # Suite de validación y evaluación automatizada
├── dataset_generator.py              # Generador del dataset instruccional
├── train_styleai_llm.py              # Script de fine-tuning (QLoRA / PEFT)
├── inference_llm.py                  # Script de inferencia y prueba de modelos de lenguaje
├── fine_tune_styleai.ipynb           # Cuaderno de experimentación para Google Colab
├── DiegoFabianAndrade_...Demo.mp4    # Video demostrativo de la solución
└── README.md                         # Documentación técnica integral
```

---

## ⚙️ 4. Arquitectura Técnica y Funcionalidades del MVP

### A. Motor de Recomendación Heurístico y Adaptativo
El motor evalúa las combinaciones candidatas del armario mediante una función de compatibilidad global:

$$\text{Puntaje Total} = 0.35 \cdot S_{\text{formalidad}} + 0.35 \cdot S_{\text{térmico}} + 0.20 \cdot S_{\text{color}} + 0.10 \cdot S_{\text{estilo}}$$

- **Puntaje de Formalidad ($S_{\text{formalidad}}$):** Penaliza de forma lineal la desviación entre el promedio de formalidad de las prendas seleccionadas y la formalidad objetivo de la ocasión.
- **Puntaje Térmico ($S_{\text{térmico}}$):** Comprueba si el promedio térmico del conjunto se encuentra dentro del rango de tolerancia exigido por el clima actual.
- **Puntaje de Color ($S_{\text{color}}$):** Aplica principios de armonía cromática favoreciendo bases neutras (negro, blanco, gris, beige) y combinaciones clásicas equilibradas.
- **Bono de Estilo ($S_{\text{estilo}}$):** Bonifica las combinaciones cuyas prendas coinciden con la preferencia seleccionada por el usuario.

### B. Endpoints del Servicio Backend (`app_backend.py`)
El servicio backend expone una API REST construida sobre FastAPI:
- `GET /api/health`: Estado del servicio, versión del MVP y métricas acumuladas.
- `POST /api/recommend`: Recibe el estado del armario, clima y ocasión, devolviendo el ranking ordenado de outfits con desglose detallado de puntajes, justificación técnica y latencia en milisegundos.
- `POST /api/feedback`: Registra la calificación del usuario (`like`/`dislike`, puntaje numérico 1-5 y comentarios), persistiendo la información en `data/user_feedback.json`.
- `GET /api/metrics`: Retorna métricas de rendimiento en tiempo real (latencia promedio, afinidad media de las recomendaciones y porcentaje de satisfacción).
- `POST /api/evaluate`: Ejecuta automáticamente la batería de escenarios de prueba y retorna los resultados de verificación de restricciones.

### C. Módulo de Gestión de Armario
- Registro dinámico de nuevas prendas con validación de categorías y atributos (1 a 5).
- Soporte de exportación completa del catálogo a formato JSON (`📥 Exportar`).
- Soporte de importación de armarios externos desde archivo JSON (`📤 Importar`).
- Restablecimiento seguro al catálogo predeterminado de demostración (`🔄 Restablecer`).

---

## 🧪 5. Resultados de Evaluación y Validación Técnica

Para validar la viabilidad técnica de la solución y comprobar el cumplimiento de las restricciones, se implementó una batería de pruebas automatizada (`test_evaluacion.py` y endpoint `/api/evaluate`):

| Prueba / Escenario | Condiciones de Entrada | Criterio de Aceptación | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **1. Restricciones Térmicas (Clima Frío)** | Clima frío (<12°C), Lluvia, Formal | Nivel térmico promedio $\ge 3.5$ y presencia de prenda exterior | Nivel térmico: **4.25 / 5.0** con abrigo impermeable | ✅ APROBADO |
| **2. Restricciones Térmicas (Clima Cálido)** | Clima cálido (>24°C), Soleado, Casual | Nivel térmico promedio $\le 2.5$ sin capas innecesarias | Nivel térmico: **1.67 / 5.0** | ✅ APROBADO |
| **3. Restricciones de Formalidad (Gala)** | Evento formal de etiqueta / gala | Nivel de formalidad del conjunto $\ge 4.0$ | Formalidad: **4.67 / 5.0** | ✅ APROBADO |
| **4. Integridad y Coherencia de Catálogo** | Catálogo completo de prendas | Todas las prendas poseen atributos válidos (1-5) y categorías correctas | **100%** de prendas consistentes | ✅ APROBADO |
| **5. Rendimiento y Latencia de Inferencia** | Evaluación sobre catálogo completo | Tiempo de procesamiento y ranking $< 50 \text{ ms}$ | **~3.8 ms** promedio por consulta | ✅ APROBADO |

**Resumen de Validación:** 5 de 5 pruebas superadas con éxito (**100% de tasa de aprobación**). El reporte detallado se genera en `data/resultados_evaluacion.json`.

---

## 🚀 6. Guía de Ejecución del Sistema

### Opción A: Ejecución Rápida del Prototipo Web (Frontend Autónomo)
El frontend incluye modo local autónomo, lo que permite probarlo inmediatamente sin requerir dependencias adicionales:
1. Navega a la carpeta `styleai_app/`.
2. Abre `index.html` en cualquier navegador web moderno (Chrome, Edge, Firefox, Brave).
3. Utiliza la barra superior para revisar el estado del sistema, generar recomendaciones y navegar por la pestaña **📊 Métricas & Validación** para ejecutar la batería de pruebas en vivo.

### Opción B: Ejecución Completa con Backend API (Python)
Para habilitar el servicio backend y la sincronización en tiempo real:

```bash
# 1. Instalar dependencias del backend
pip install fastapi uvicorn pydantic

# 2. Iniciar el servidor API local
python app_backend.py
```

El servidor quedará disponible en `http://127.0.0.1:8000`. Al abrir `styleai_app/index.html`, el indicador de conexión cambiará automáticamente a **API Activa (v2.0)**.

### Opción C: Ejecutar la Suite de Pruebas Automatizadas
Para verificar el comportamiento del motor de recomendación por consola:

```bash
python test_evaluacion.py
```

---

## 📋 7. Matriz de Cumplimiento de Entregables — Hito 3

| Entregable del Hito 3 | Estado | Detalle y Ubicación de las Evidencias |
| :--- | :---: | :--- |
| **Documento: Diseñar, implementar y validar la solución** | ✍️ A cargo del estudiante | Estructura técnica, métricas obtenidas, justificación de arquitectura y resultados de evaluación detallados en este repositorio para soporte del documento final de entrega. |
| **Prototipo funcional MVP** | ✅ Implementado | Prototipo web funcional en [`styleai_app/index.html`](styleai_app/index.html) con lógica de recomendación, retroalimentación de usuario y validación en vivo. |
| **Versión final solución: Fuentes del diseño y del código** | ✅ Implementado | Fuentes organizadas en `styleai_app/` (diseño y frontend), `app_backend.py` (API backend) y scripts de soporte (`test_evaluacion.py`, `dataset_generator.py`). |
| **Video (máx 10 min) presentando resultados y demo del MVP** | 🎥 Grabado / A cargo del estudiante | Archivo de demostración referenciado e integrado en la interfaz ([`DiegoFabianAndrade_PROYECTO-PTIA-STYLEAI-DIEGO-ANDRADE_Demo.mp4`](DiegoFabianAndrade_PROYECTO-PTIA-STYLEAI-DIEGO-ANDRADE_Demo.mp4)). |

---

© 2026 **StyleAI** — Proyecto de Inteligencia Artificial Aplicada (PTIA) | Escuela Colombiana de Ingeniería Julio Garavito | Diego Andrade
