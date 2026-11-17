import time
import json
import os
import sys
from app_backend import (
    Item, RecommendRequest, evaluate_outfit_combination,
    check_color_harmony, OCCASION_TARGETS, WEATHER_TARGETS
)

def create_sample_wardrobe():
    return [
        Item(id="1", name="Camisa Oxford Blanca", category="top", color="blanco", warmth=2, formality=4, style="elegante"),
        Item(id="2", name="Camiseta Negra Básica", category="top", color="negro", warmth=1, formality=1, style="casual"),
        Item(id="3", name="Buzo de Lana Gris", category="top", color="gris", warmth=4, formality=2, style="casual"),
        Item(id="4", name="Chaqueta de Jean", category="outerwear", color="azul", warmth=3, formality=2, style="urbano"),
        Item(id="5", name="Abrigo Paño Negro", category="outerwear", color="negro", warmth=5, formality=5, style="elegante"),
        Item(id="6", name="Jeans Azules Oscuros", category="bottom", color="azul", warmth=3, formality=2, style="casual"),
        Item(id="7", name="Pantalón de Vestir Negro", category="bottom", color="negro", warmth=3, formality=5, style="elegante"),
        Item(id="8", name="Pantalón Chino Beige", category="bottom", color="beige", warmth=2, formality=3, style="casual"),
        Item(id="9", name="Tenis Blancos Urbano", category="shoes", color="blanco", warmth=2, formality=1, style="urbano"),
        Item(id="10", name="Zapatos de Cuero Café", category="shoes", color="cafe", warmth=3, formality=5, style="elegante"),
        Item(id="11", name="Botas de Cuero Negras", category="shoes", color="negro", warmth=4, formality=3, style="urbano"),
        Item(id="12", name="Sudadera Deportiva Gris", category="bottom", color="gris", warmth=2, formality=1, style="deportivo")
    ]

def test_restricciones_termicas():
    wardrobe = create_sample_wardrobe()
    tops = [i for i in wardrobe if i.category == "top"]
    bottoms = [i for i in wardrobe if i.category == "bottom"]
    shoes = [i for i in wardrobe if i.category == "shoes"]
    outers = [i for i in wardrobe if i.category == "outerwear"] + [None]

    climates = ["frio", "templado", "calido", "lluvioso"]
    results = []

    for clim in climates:
        best_score = -1
        best_outfit = None
        for t in tops:
            for b in bottoms:
                for s in shoes:
                    for o in outers:
                        res = evaluate_outfit_combination(t, b, s, o, "casual", clim, "casual")
                        if res["score"] > best_score:
                            best_score = res["score"]
                            best_outfit = res

        target_w = WEATHER_TARGETS[clim]["warmth"]
        avg_w = best_outfit["breakdown"]["avgWarmth"]
        diff = abs(avg_w - target_w)
        passed = diff <= 1.5

        results.append({
            "clima": clim,
            "targetWarmth": target_w,
            "avgWarmth": avg_w,
            "diff": round(diff, 1),
            "score": best_score,
            "passed": passed
        })

    all_passed = all(r["passed"] for r in results)
    return {"name": "Restricciones Térmicas", "passed": all_passed, "details": results}

def test_restricciones_formalidad():
    wardrobe = create_sample_wardrobe()
    tops = [i for i in wardrobe if i.category == "top"]
    bottoms = [i for i in wardrobe if i.category == "bottom"]
    shoes = [i for i in wardrobe if i.category == "shoes"]
    outers = [i for i in wardrobe if i.category == "outerwear"] + [None]

    occasions = ["trabajo", "formal", "casual", "deporte", "fiesta", "cita"]
    results = []

    for occ in occasions:
        best_score = -1
        best_outfit = None
        for t in tops:
            for b in bottoms:
                for s in shoes:
                    for o in outers:
                        res = evaluate_outfit_combination(t, b, s, o, occ, "templado", "casual")
                        if res["score"] > best_score:
                            best_score = res["score"]
                            best_outfit = res

        target_f = OCCASION_TARGETS[occ]["formality"]
        avg_f = best_outfit["breakdown"]["avgFormality"]
        diff = abs(avg_f - target_f)
        passed = diff <= 1.5

        results.append({
            "ocasion": occ,
            "targetFormality": target_f,
            "avgFormality": avg_f,
            "diff": round(diff, 1),
            "score": best_score,
            "passed": passed
        })

    all_passed = all(r["passed"] for r in results)
    return {"name": "Restricciones de Formalidad", "passed": all_passed, "details": results}

def test_consistencia_catalogo():
    wardrobe = create_sample_wardrobe()
    valid_ids = {i.id for i in wardrobe}
    valid_names = {i.name for i in wardrobe}

    tops = [i for i in wardrobe if i.category == "top"]
    bottoms = [i for i in wardrobe if i.category == "bottom"]
    shoes = [i for i in wardrobe if i.category == "shoes"]

    inconsistencies = 0
    total_evaluated = 0

    for t in tops:
        for b in bottoms:
            for s in shoes:
                res = evaluate_outfit_combination(t, b, s, None, "casual", "templado", "casual")
                total_evaluated += 1

                for piece_key in ["top", "bottom", "shoes"]:
                    piece = res[piece_key]
                    if piece["id"] not in valid_ids or piece["name"] not in valid_names:
                        inconsistencies += 1

    passed = (inconsistencies == 0) and (total_evaluated > 0)
    return {
        "name": "Consistencia de Catálogo",
        "passed": passed,
        "totalEvaluated": total_evaluated,
        "inconsistencies": inconsistencies,
        "integrityRate": 100.0 if passed else 0.0
    }

def test_armonia_colores():
    # Pares conocidos armónicos
    score_bw = check_color_harmony("blanco", "negro", "negro")
    score_neutral = check_color_harmony("gris", "blanco", "beige")
    score_contrast = check_color_harmony("azul", "beige", "cafe")

    passed = (score_bw >= 85) and (score_neutral >= 80) and (score_contrast >= 70)
    return {
        "name": "Armonía de Colores",
        "passed": passed,
        "scoreBlancoNegro": score_bw,
        "scoreNeutros": score_neutral,
        "scoreContraste": score_contrast
    }

def test_latencia_rendimiento(num_iterations=50):
    wardrobe = create_sample_wardrobe()
    tops = [i for i in wardrobe if i.category == "top"]
    bottoms = [i for i in wardrobe if i.category == "bottom"]
    shoes = [i for i in wardrobe if i.category == "shoes"]
    outers = [i for i in wardrobe if i.category == "outerwear"] + [None]

    latencies = []
    for _ in range(num_iterations):
        t0 = time.time()
        for t in tops:
            for b in bottoms:
                for s in shoes:
                    for o in outers:
                        _ = evaluate_outfit_combination(t, b, s, o, "trabajo", "frio", "elegante")
        elapsed = (time.time() - t0) * 1000
        latencies.append(elapsed)

    avg_ms = round(sum(latencies) / len(latencies), 2)
    max_ms = round(max(latencies), 2)
    min_ms = round(min(latencies), 2)
    passed = avg_ms < 50.0  # Meta estricta de tiempo de respuesta

    return {
        "name": "Rendimiento y Latencia",
        "passed": passed,
        "iterations": num_iterations,
        "avgLatencyMs": avg_ms,
        "maxLatencyMs": max_ms,
        "minLatencyMs": min_ms,
        "targetMaxMs": 50.0
    }

def run_all_tests():
    print("=" * 65)
    print(" StyleAI — Suite de Validación y Evaluación Técnica (Hito 3)")
    print("=" * 65)

    tests = [
        test_restricciones_termicas(),
        test_restricciones_formalidad(),
        test_consistencia_catalogo(),
        test_armonia_colores(),
        test_latencia_rendimiento(50)
    ]

    total = len(tests)
    passed = sum(1 for t in tests if t["passed"])
    pass_rate = round((passed / total) * 100, 1)

    for i, t in enumerate(tests, 1):
        status = "✅ APROBADO" if t["passed"] else "❌ FALLIDO"
        print(f"[{i}/{total}] {t['name']:<32} {status}")

    print("-" * 65)
    print(f"Resultado Global: {passed}/{total} Pruebas Superadas ({pass_rate}%)")
    print("=" * 65)

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    report_file = os.path.join(output_dir, "resultados_evaluacion.json")

    report_payload = {
        "timestamp": time.time(),
        "title": "Evaluación de Desempeño y Validación Técnica StyleAI MVP",
        "hito": "Hito 3 - Solución y Evaluación",
        "totalTests": total,
        "passed": passed,
        "passRate": pass_rate,
        "tests": tests
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2, ensure_ascii=False)

    print(f"Reporte detallado guardado exitosamente en: {report_file}")
    return report_payload

if __name__ == "__main__":
    report = run_all_tests()
    if report["passRate"] < 100:
        sys.exit(1)
    sys.exit(0)
