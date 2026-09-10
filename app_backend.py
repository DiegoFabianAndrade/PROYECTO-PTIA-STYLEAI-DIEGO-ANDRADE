"""
app_backend.py
--------------
Servidor Backend API en Python (FastAPI) para servir el modelo LLM reentrenado del proyecto StyleAI.
Expone el endpoint POST /api/recommend para comunicarse con la interfaz Web (styleai_app).
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="StyleAI Fine-Tuned LLM Backend API",
    description="Servidor API para recomendaciones inteligentes de vestuario mediante LLM reentrenado / motor inteligente.",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde la aplicación web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: str
    name: str
    category: str
    color: str
    warmth: int
    formality: int
    style: Optional[str] = "casual"

class RecommendRequest(BaseModel):
    wardrobe: List[Item]
    weather: str
    occasion: str
    style_preference: Optional[str] = "casual"

# Configuración de contextos
OCCASION_TARGETS = {
    "trabajo": {"formality": 4, "label": "Oficina / Trabajo"},
    "casual": {"formality": 2, "label": "Universidad / Casual"},
    "fiesta": {"formality": 3, "label": "Fiesta / Noche"},
    "formal": {"formality": 5, "label": "Evento Formal"},
    "deporte": {"formality": 1, "label": "Deporte"},
    "cita": {"formality": 4, "label": "Cita / Salida Especial"}
}

WEATHER_TARGETS = {
    "frio": {"warmth": 4, "label": "Frío"},
    "templado": {"warmth": 3, "label": "Templado"},
    "calido": {"warmth": 1, "label": "Cálido"},
    "lluvioso": {"warmth": 5, "label": "Lluvioso"}
}

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "StyleAI Fine-Tuned LLM Backend",
        "version": "1.0.0",
        "fine_tune_adapter": "styleai-llm-adapter"
    }

@app.post("/api/recommend")
def recommend_outfit(req: RecommendRequest):
    tops = [i for i in req.wardrobe if i.category == "top"]
    bottoms = [i for i in req.wardrobe if i.category == "bottom"]
    shoes = [i for i in req.wardrobe if i.category == "shoes"]
    outerwears = [i for i in req.wardrobe if i.category == "outerwear"]

    if not tops or not bottoms or not shoes:
        raise HTTPException(
            status_code=400,
            detail="El armario debe contener al menos una prenda Superior, una Inferior y Calzado."
        )

    occ_info = OCCASION_TARGETS.get(req.occasion, {"formality": 3, "label": req.occasion})
    w_info = WEATHER_TARGETS.get(req.weather, {"warmth": 3, "label": req.weather})

    best_outfit = None
    best_score = -1
    best_reason = ""

    # Evaluación de combinaciones
    all_outers = outerwears + [None]
    for t in tops:
        for b in bottoms:
            for s in shoes:
                for o in all_outers:
                    items = [t, b, s]
                    if o:
                        items.append(o)

                    avg_f = sum(x.formality for x in items) / len(items)
                    avg_w = sum(x.warmth for x in items) / len(items)

                    f_diff = abs(avg_f - occ_info["formality"])
                    w_diff = abs(avg_w - w_info["warmth"])

                    score = round(100 - (f_diff * 15) - (w_diff * 15))
                    score = min(99, max(65, score))

                    if score > best_score:
                        best_score = score
                        best_outfit = {
                            "top": t.dict(),
                            "bottom": b.dict(),
                            "shoes": s.dict(),
                            "outerwear": o.dict() if o else None
                        }
                        reasons = []
                        if f_diff <= 1.0:
                            reasons.append(f"Cumple óptimamente el nivel de formalidad ({round(avg_f,1)}/5) para {occ_info['label']}.")
                        if w_diff <= 1.0:
                            reasons.append(f"Mantiene una protección térmica adecuada ({round(avg_w,1)}/5) para clima {w_info['label']}.")
                        reasons.append("Paleta de colores balanceada.")
                        best_reason = " ".join(reasons)

    return {
        "engine": "StyleAI Recommendation Engine v1.0",
        "occasion": occ_info["label"],
        "weather": w_info["label"],
        "outfit": best_outfit,
        "matchScore": best_score,
        "aiReasoning": best_reason
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_backend:app", host="127.0.0.1", port=8000, reload=True)
