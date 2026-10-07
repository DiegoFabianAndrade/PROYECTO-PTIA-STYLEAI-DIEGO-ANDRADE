# StyleAI — Recomendador de Outfits y Gestión de Armario Inteligente

> **Escuela Colombiana de Ingeniería Julio Garavito**  
> **Asignatura / Programa:** Proyecto PTIA  
> **Autor:** Diego Andrade  
> **Entrega Evaluada:** Hito 2 — Problema y Avances en la Solución (2º Tercio - Semana 10)  
> **Estado del Prototipo:** Versión Preliminar Navegable, Funcional e Interactiva v1.0

---

## 📌 1. Descripción del Proyecto y Propósito

**StyleAI** es un sistema inteligente diseñado para resolver la fatiga de decisión diaria en la selección de prendas de vestir. Combina una interfaz de usuario interactiva y navegable con un algoritmo de recomendación contextualmente adaptativo que evalúa variables clave como el **clima**, la **ocasión** (oficina, universidad, eventos formales, citas, deporte) y las **preferencias de estilo personal**.

### 🎯 Problema que Resuelve
Seleccionar el vestuario adecuado diariamente suele requerir tiempo y esfuerzo mental para conciliar la protección térmica, el nivel de formalidad exigido por el entorno y la combinación cromática de las prendas disponibles en el armario.

### 💡 Solución Propuesta
StyleAI ofrece un entorno digital integral compuesto por:
1. **Gestión Digital de Armario:** Registro estructurado de prendas individuales con parámetros de nivel térmico (1-5), etiqueta de formalidad (1-5), categoría (superior, inferior, calzado, abrigo) y color primario.
2. **Motor de Recomendación Adaptativo:** Evaluador de combinaciones que calcula el porcentaje de compatibilidad de conjunto (*Match %*) y justifica la elección óptima.
3. **Prototipo Web de Alta Fidelidad:** Interfaz navegable basada en patrones de diseño contemporáneos (*Mobbin* y *HumaneByDesign*), con tarjetas colapsables, menús contenidos y simulaciones en tiempo real.

---

## 🏆 2. Evidencias de la Entrega (Hito 2: Problema y Avances en la Solución)

Este repositorio contiene la evidencia completa de los entregables del **Hito 2**:

### 📄 A. Documento y Justificación Metodológica y Técnica
- **Documento Adjunto de la Entrega:** [`Plantilla_Proyectos_PTIA_ECI_DiegoAndrade_Entrega2.docx`](Plantilla_Proyectos_PTIA_ECI_DiegoAndrade_Entrega2.docx)
- **Arquitectura de Recomendación:** Integración de un modelo en Python con cuantización de 4-bits (**QLoRA**) y adaptadores **PEFT** sobre arquitecturas de lenguaje instruccionales (`Qwen2.5-1.5B-Instruct` / `Llama-3.2-1B`).
- **Dataset Sintético Instruccional:** Generación automatizada de 500 muestras en formato JSONL (`data/styleai_dataset.jsonl`) simulando armarios de usuarios y contextos diversos.
- **Servidor Backend API:** Servicio web dinámico en **FastAPI** (`app_backend.py`) que expone el endpoint `POST /api/recommend` para inferencias remota/local.

### 🎨 B. Prototipo de Interfaz (Navegable y Funcional)
De acuerdo con las especificaciones del Hito 2, el prototipo cumple con ser una **versión preliminar navegable** diseñada para validar la experiencia de usuario (UX) e incluir simulaciones de funciones:
- **Ubicación del Prototipo:** [`styleai_app/index.html`](styleai_app/index.html) (se ejecuta directamente en cualquier navegador moderno sin requerir compilación).
- **Características Clave de UX/UI:**
  - **Diseño de Alto Contraste:** Estética en obsidiana profunda (`#03050d`), tarjetas slate (`#0d1527`), bordes violáceos de 2px y resaltados neón.
  - **Desplegables Interactivos (Acordeones):** Módulos colapsables para *Contexto y Preferencias*, *Gestión de Armario*, *Guía de Estilo Inteligente* y *Desglose Técnico de Compatibilidad*.
  - **Contención de Menús (`custom-dropdown`):** Menús personalizados que eliminan el desbordamiento de selectores nativos.
  - **Carrusel de Tendencias:** Explorador horizontal dinámico (`🔥 Combinaciones Destacadas de Hoy`).
  - **Simulación de Funciones Futuras:** Generación aleatoria (*🎲 Sorpréndeme*), sistema de favoritos con persistencia local (*⭐ Mis Favoritos*), inspector modal de detalles (*🔍 Detalle*), copia al portapapeles y visualización de métricas KPI.

### 💻 C. Avances en la Solución (Fuentes del Diseño y Código)
Estructura organizada de los componentes desarrollados en el proyecto:

```text
PROYECTO-PTIA-STYLEAI-DIEGO-ANDRADE/
├── styleai_app/                 # FUENTES DEL DISEÑO (Frontend Web Navegable)
│   ├── index.html               # Estructura principal y maquetación HTML5
│   ├── style.css                # Sistema de diseño de alto contraste, tokens y animaciones
│   ├── app.js                   # Lógica de interacción, almacenamiento local y renderizado
│   └── assets/                  # Recursos gráficos y vectoriales
│       ├── logo.png             # Logotipo oficial de la marca
│       ├── top.svg              # Vector de categoría prendas superiores
│       ├── bottom.svg           # Vector de categoría prendas inferiores
│       ├── shoes.svg            # Vector de categoría calzado
│       └── outerwear.svg        # Vector de categoría abrigos y sacos
├── data/                        # FUENTES DE DATOS
│   └── styleai_dataset.jsonl    # Dataset instruccional generado (500 ejemplos)
├── app_backend.py               # Servidor API backend en FastAPI
├── dataset_generator.py         # Script generador de dataset instruccional
├── train_styleai_llm.py         # Script de Fine-Tuning QLoRA / PEFT
├── inference_llm.py             # Script de evaluación e inferencia local
├── fine_tune_styleai.ipynb      # Notebook de entrenamiento para Google Colab
└── README.md                    # Documentación general del proyecto
```

### 🎬 D. Video Corto de Presentación de Avances (Máx 5 Minutos)
- **Archivo de Video Adjunto:** [`DiegoFabianAndrade_PROYECTO-PTIA-STYLEAI-DIEGO-ANDRADE_Demo.mp4`](DiegoFabianAndrade_PROYECTO-PTIA-STYLEAI-DIEGO-ANDRADE_Demo.mp4)
- **Contenido del Video:** Presentación integral de la totalidad de los desarrollos del Hito 2:
  1. **Justificación Metodológica y Técnica:** Explicación del modelo de recomendación, dataset instruccional JSONL y API FastAPI.
  2. **Demostración Navegable del Prototipo:** Recorrido interactivo por la interfaz web (`styleai_app/`), desplegables acordeón, carrusel de tendencias, filtros en vivo y simulación de funciones.
  3. **Revisión de Fuentes:** Exposición de la estructura de código fuente y fuentes de diseño desarrolladas en el repositorio.

---

## 🚀 3. Guía de Uso y Ejecución del Proyecto

### Opción 1: Probar el Prototipo Navegable (Frontend)
1. Descarga o clona este repositorio en tu sistema local.
2. Abre la carpeta `styleai_app/`.
3. Haz doble clic en el archivo `index.html` (o ábrelo con tu navegador web preferido: Chrome, Edge, Firefox, Safari).
4. Acciones navegables disponibles:
   - Haz clic en **✨ Generar Combinaciones** tras ajustar el clima o la ocasión.
   - Haz clic en **🎲 Sorpréndeme** para probar la generación aleatoria.
   - Registra prendas nuevas en el desplegable **Gestión de Armario**.
   - Haz clic en **📊 Desglose de Compatibilidad** dentro de cualquier tarjeta de outfit.
   - Explora las cápsulas de demostración (*Minimalista*, *Ejecutivo*, *Urbano*).

### Opción 2: Ejecutar el Servidor Backend API (Python)
Para ejecutar el servidor de recomendación en Python:

```bash
# 1. Instalar dependencias requeridas
pip install fastapi uvicorn pydantic torch transformers peft datasets

# 2. Generar el dataset de entrenamiento
python dataset_generator.py

# 3. Iniciar el servidor API local
python app_backend.py
```
El servidor backend se iniciará en `http://127.0.0.1:8000` exponiendo los endpoints de consulta.

---

## 📊 4. Matriz de Cumplimiento de Hito 2

| Criterio Evaluado | Estado | Evidencia en el Repositorio |
| :--- | :---: | :--- |
| **Documento y Justificación Técnica** | ✅ Completo | Implementación del servidor API (`app_backend.py`), scripts de entrenamiento (`train_styleai_llm.py`) y dataset (`styleai_dataset.jsonl`). |
| **Prototipo de Interfaz Navegable** | ✅ Completo | Interfaz web interactiva en `styleai_app/index.html` con simulación de funciones y validación de UX. |
| **Avances en la Solución (Fuentes)** | ✅ Completo | Código fuente organizado en `styleai_app/` (diseño) y scripts `.py` (lógica del modelo). |
| **Video Corto de Avances (5 min)** | ⏳ Pendiente | Reservado para adjuntar enlace final. |

---

© 2026 **StyleAI** — Proyecto PTIA | Escuela Colombiana de Ingeniería Julio Garavito | Diego Andrade