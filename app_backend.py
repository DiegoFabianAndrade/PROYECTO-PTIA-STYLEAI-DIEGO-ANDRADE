import time
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI(
    title="StyleAI — API del Motor de Recomendación",
    description="Servidor API para evaluación y recomendación de vestuario según contexto climático y de formalidad.",
    version="2.0.0-mvp"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Almacenamiento en memoria para métricas y feedback del MVP
METRICS_DATA = {
    "total_recommendations": 0,
    "total_latency_ms": 0.0,
    "total_score_sum": 0.0,
    "feedback_positive": 0,
    "feedback_negative": 0
}

FEEDBACK_FILE = "data/user_feedback.json"

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
    limit: Optional[int] = 4

class FeedbackRequest(BaseModel):
    outfit_id: Optional[str] = None
    rating: str  # "like" o "dislike"
    score: Optional[int] = 5
    comment: Optional[str] = None

OCCASION_TARGETS = {
    "trabajo": {"formality": 4, "label": "Oficina / Trabajo"},
    "casual": {"formality": 2, "label": "Universidad / Casual"},
    "fiesta": {"formality": 3, "label": "Fiesta / Noche"},
    "formal": {"formality": 5, "label": "Evento Formal"},
    "deporte": {"formality": 1, "label": "Deporte"},
    "cita": {"formality": 4, "label": "Cita / Salida Especial"}
}

WEATHER_TARGETS = {
    "frio": {"warmth": 4, "label": "Frío (<12°C)"},
    "templado": {"warmth": 3, "label": "Templado (12°C - 20°C)"},
    "calido": {"warmth": 1, "label": "Cálido (>20°C)"},
    "lluvioso": {"warmth": 5, "label": "Lluvioso / Húmedo"}
}

NEUTRAL_COLORS = ["negro", "blanco", "gris", "beige"]

def check_color_harmony(c1: str, c2: str, c3: str) -> int:
    score = 70
    neutrals = [c for c in [c1, c2, c3] if c.lower() in NEUTRAL_COLORS]
    if len(neutrals) >= 2:
        score += 20
    if (c1 == "negro" and c2 == "blanco") or (c1 == "blanco" and c2 == "negro"):
        score += 10
    if (c1 == "azul" and c2 == "beige") or (c1 == "beige" and c2 == "azul"):
        score += 10
    if c1 == c2:
        score += 10
    return min(100, score)

def evaluate_outfit_combination(top, bottom, shoes, outerwear, occasion_key: str, weather_key: str, preferred_style: str):
    occ_info = OCCASION_TARGETS.get(occasion_key, {"formality": 2, "label": occasion_key})
    w_info = WEATHER_TARGETS.get(weather_key, {"warmth": 3, "label": weather_key})

    items = [top, bottom, shoes]
    if outerwear:
        items.append(outerwear)

    # 1. Formalidad
    avg_f = sum(x.formality for x in items) / len(items)
    f_diff = abs(avg_f - occ_info["formality"])
    formality_score = max(0, 100 - f_diff * 25)

    # 2. Abrigo térmico
    avg_w = sum(x.warmth for x in items) / len(items)
    w_diff = abs(avg_w - w_info["warmth"])
    warmth_score = max(20, 100 - w_diff * 25)

    # 3. Armonía de color
    color_score = check_color_harmony(top.color, bottom.color, shoes.color)

    # 4. Bonificación de estilo
    style_matches = sum(1 for x in items if getattr(x, "style", "casual") == preferred_style)
    style_score = (style_matches / len(items)) * 100

    # Ponderación compuesta
    total_score = round(
        formality_score * 0.35 +
        warmth_score * 0.35 +
        color_score * 0.20 +
        style_score * 0.10
    )
    total_score = min(99, max(60, total_score))

    reasons = []
    if f_diff <= 0.8:
        reasons.append(f"Cumple óptimamente el nivel de formalidad ({round(avg_f, 1)}/5) para {occ_info['label']}.")
    elif f_diff <= 1.5:
        reasons.append(f"Nivel de formalidad equilibrado ({round(avg_f, 1)}/5) para la ocasión.")

    if w_diff <= 0.8:
        reasons.append(f"Protección térmica adecuada ({round(avg_w, 1)}/5) para clima {w_info['label']}.")
    elif w_diff <= 1.5:
        reasons.append(f"Abrigo térmico aceptable para las condiciones climáticas.")

    if color_score >= 80:
        reasons.append(f"Excelente combinación cromática entre {top.color}, {bottom.color} y {shoes.color}.")

    reasoning_text = " ".join(reasons) if reasons else "Combinación equilibrada entre las prendas disponibles."

    return {
        "top": top.dict() if hasattr(top, "dict") else top,
        "bottom": bottom.dict() if hasattr(bottom, "dict") else bottom,
        "shoes": shoes.dict() if hasattr(shoes, "dict") else shoes,
        "outerwear": (outerwear.dict() if hasattr(outerwear, "dict") else outerwear) if outerwear else None,
        "score": total_score,
        "breakdown": {
            "formalityScore": round(formality_score, 1),
            "warmthScore": round(warmth_score, 1),
            "colorScore": round(color_score, 1),
            "styleScore": round(style_score, 1),
            "avgFormality": round(avg_f, 1),
            "avgWarmth": round(avg_w, 1)
        },
        "reasoning": reasoning_text
    }

@app.get("/")
@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "StyleAI Recommendation API",
        "version": "2.0.0-mvp",
        "engine": "StyleAI Adaptive Engine",
        "metrics": {
            "totalRecommendations": METRICS_DATA["total_recommendations"],
            "feedbackReceived": METRICS_DATA["feedback_positive"] + METRICS_DATA["feedback_negative"]
        }
    }

@app.post("/api/recommend")
def recommend_outfits(req: RecommendRequest):
    start_time = time.time()

    tops = [i for i in req.wardrobe if i.category == "top"]
    bottoms = [i for i in req.wardrobe if i.category == "bottom"]
    shoes = [i for i in req.wardrobe if i.category == "shoes"]
    outerwears = [i for i in req.wardrobe if i.category == "outerwear"]

    if not tops or not bottoms or not shoes:
        raise HTTPException(
            status_code=400,
            detail="El armario debe contener al menos una prenda Superior, una Inferior y Calzado."
        )

    occ_info = OCCASION_TARGETS.get(req.occasion, {"formality": 2, "label": req.occasion})
    w_info = WEATHER_TARGETS.get(req.weather, {"warmth": 3, "label": req.weather})

    all_candidates = []
    outer_options = outerwears + [None]

    for t in tops:
        for b in bottoms:
            for s in shoes:
                for o in outer_options:
                    res = evaluate_outfit_combination(t, b, s, o, req.occasion, req.weather, req.style_preference or "casual")
                    all_candidates.append(res)

    all_candidates.sort(key=lambda x: x["score"], reverse=True)
    limit = req.limit or 4
    top_outfits = all_candidates[:limit]
    best_outfit = top_outfits[0] if top_outfits else None

    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    # Actualizar métricas acumuladas
    if best_outfit:
        METRICS_DATA["total_recommendations"] += 1
        METRICS_DATA["total_latency_ms"] += elapsed_ms
        METRICS_DATA["total_score_sum"] += best_outfit["score"]

    return {
        "engine": "StyleAI Recommendation Engine v2.0-MVP",
        "occasion": occ_info["label"],
        "weather": w_info["label"],
        "outfit": best_outfit,
        "outfits": top_outfits,
        "matchScore": best_outfit["score"] if best_outfit else 0,
        "reasoning": best_outfit["reasoning"] if best_outfit else "",
        "evaluatedCombinations": len(all_candidates),
        "latencyMs": elapsed_ms
    }

@app.post("/api/feedback")
def submit_feedback(fb: FeedbackRequest):
    if fb.rating == "like":
        METRICS_DATA["feedback_positive"] += 1
    else:
        METRICS_DATA["feedback_negative"] += 1

    total_fb = METRICS_DATA["feedback_positive"] + METRICS_DATA["feedback_negative"]
    satisfaction = round((METRICS_DATA["feedback_positive"] / total_fb) * 100, 1) if total_fb > 0 else 100.0

    try:
        os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
        record = {
            "timestamp": time.time(),
            "rating": fb.rating,
            "score": fb.score,
            "comment": fb.comment
        }
        with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass

    return {
        "status": "success",
        "message": "Retroalimentación registrada correctamente",
        "totalFeedback": total_fb,
        "satisfactionRate": satisfaction
    }

@app.get("/api/metrics")
def get_metrics():
    total_recs = METRICS_DATA["total_recommendations"]
    avg_latency = round(METRICS_DATA["total_latency_ms"] / total_recs, 2) if total_recs > 0 else 0.0
    avg_score = round(METRICS_DATA["total_score_sum"] / total_recs, 1) if total_recs > 0 else 0.0
    total_fb = METRICS_DATA["feedback_positive"] + METRICS_DATA["feedback_negative"]
    satisfaction = round((METRICS_DATA["feedback_positive"] / total_fb) * 100, 1) if total_fb > 0 else 100.0

    return {
        "totalRecommendations": total_recs,
        "averageLatencyMs": avg_latency,
        "averageMatchScore": avg_score,
        "satisfactionRate": satisfaction,
        "totalFeedback": total_fb,
        "positiveFeedback": METRICS_DATA["feedback_positive"],
        "negativeFeedback": METRICS_DATA["feedback_negative"]
    }

@app.post("/api/evaluate")
def run_evaluation_suite():
    # Casos de prueba estándar para validar la solución
    test_wardrobe = [
        Item(id="t1", name="Camisa Oxford Blanca", category="top", color="blanco", warmth=2, formality=4, style="elegante"),
        Item(id="t2", name="Camiseta Negra Básica", category="top", color="negro", warmth=1, formality=1, style="casual"),
        Item(id="t3", name="Buzo de Lana Gris", category="top", color="gris", warmth=4, formality=2, style="casual"),
        Item(id="b1", name="Pantalón de Vestir Negro", category="bottom", color="negro", warmth=3, formality=5, style="elegante"),
        Item(id="b2", name="Jeans Azules Oscuros", category="bottom", color="azul", warmth=3, formality=2, style="casual"),
        Item(id="b3", name="Pantalón Chino Beige", category="bottom", color="beige", warmth=2, formality=3, style="casual"),
        Item(id="s1", name="Zapatos de Cuero Café", category="shoes", color="cafe", warmth=3, formality=5, style="elegante"),
        Item(id="s2", name="Tenis Blancos Urbano", category="shoes", color="blanco", warmth=2, formality=1, style="urbano"),
        Item(id="s3", name="Botas de Cuero Negras", category="shoes", color="negro", warmth=4, formality=3, style="urbano"),
        Item(id="o1", name="Abrigo Paño Negro", category="outerwear", color="negro", warmth=5, formality=5, style="elegante"),
        Item(id="o2", name="Chaqueta de Jean", category="outerwear", color="azul", warmth=3, formality=2, style="urbano")
    ]

    scenarios = [
        {"name": "Oficina en Día Frío", "occasion": "trabajo", "weather": "frio", "style": "elegante", "min_score": 85},
        {"name": "Universidad Casual Templado", "occasion": "casual", "weather": "templado", "style": "casual", "min_score": 85},
        {"name": "Fiesta Nocturna", "occasion": "fiesta", "weather": "templado", "style": "urbano", "min_score": 80},
        {"name": "Evento Formal", "occasion": "formal", "weather": "frio", "style": "elegante", "min_score": 90},
        {"name": "Día Lluvioso", "occasion": "casual", "weather": "lluvioso", "style": "casual", "min_score": 80}
    ]

    start_time = time.time()
    results = []
    passed = 0

    for sc in scenarios:
        req = RecommendRequest(
            wardrobe=test_wardrobe,
            weather=sc["weather"],
            occasion=sc["occasion"],
            style_preference=sc["style"],
            limit=4
        )
        res = recommend_outfits(req)
        best = res["outfit"]
        ok = best["score"] >= sc["min_score"]
        if ok:
            passed += 1

        results.append({
            "scenario": sc["name"],
            "occasion": sc["occasion"],
            "weather": sc["weather"],
            "score": best["score"],
            "passed": ok,
            "pieces": {
                "top": best["top"]["name"],
                "bottom": best["bottom"]["name"],
                "shoes": best["shoes"]["name"],
                "outerwear": best["outerwear"]["name"] if best["outerwear"] else None
            },
            "reasoning": best["reasoning"]
        })

    elapsed_ms = round((time.time() - start_time) * 1000, 2)
    pass_rate = round((passed / len(scenarios)) * 100, 1)

    return {
        "status": "completed",
        "totalScenarios": len(scenarios),
        "passedScenarios": passed,
        "passRate": pass_rate,
        "benchmarkLatencyMs": elapsed_ms,
        "averageLatencyPerScenarioMs": round(elapsed_ms / len(scenarios), 2),
        "scenarios": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_backend:app", host="127.0.0.1", port=8000, reload=True)
