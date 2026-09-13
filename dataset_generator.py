import json
import os
import random

# Base catalog data to sample realistic combinations
TOPS = [
    {"name": "Camisa Oxford Blanca", "color": "blanco", "warmth": 2, "formality": 4, "style": "elegante"},
    {"name": "Camiseta Negra Básica", "color": "negro", "warmth": 1, "formality": 1, "style": "casual"},
    {"name": "Buzo de Lana Gris", "color": "gris", "warmth": 4, "formality": 2, "style": "casual"},
    {"name": "Camisa Azul Celeste", "color": "azul", "warmth": 2, "formality": 4, "style": "elegante"},
    {"name": "Camiseta Polo Beige", "color": "beige", "warmth": 1, "formality": 2, "style": "casual"},
    {"name": "Buzo Negro con Capucha", "color": "negro", "warmth": 3, "formality": 1, "style": "urbano"},
    {"name": "Camisa Estampada Casual", "color": "blanco", "warmth": 1, "formality": 2, "style": "casual"},
    {"name": "Suéter de Punto Marrón", "color": "marron", "warmth": 4, "formality": 3, "style": "elegante"}
]

BOTTOMS = [
    {"name": "Jeans Azules Oscuros", "color": "azul", "warmth": 3, "formality": 2, "style": "casual"},
    {"name": "Pantalón de Vestir Negro", "color": "negro", "warmth": 3, "formality": 5, "style": "elegante"},
    {"name": "Pantalón Chino Beige", "color": "beige", "warmth": 2, "formality": 3, "style": "casual"},
    {"name": "Sudadera Deportiva Gris", "color": "gris", "warmth": 2, "formality": 1, "style": "deportivo"},
    {"name": "Pantalón Chino Gris Claro", "color": "gris", "warmth": 2, "formality": 3, "style": "casual"},
    {"name": "Jeans Negros Ajustados", "color": "negro", "warmth": 3, "formality": 2, "style": "urbano"}
]

SHOES = [
    {"name": "Tenis Blancos Urbano", "color": "blanco", "warmth": 2, "formality": 1, "style": "urbano"},
    {"name": "Zapatos de Cuero Café", "color": "cafe", "warmth": 3, "formality": 5, "style": "elegante"},
    {"name": "Botas de Cuero Negras", "color": "negro", "warmth": 4, "formality": 3, "style": "urbano"},
    {"name": "Zapatos Formales Negros", "color": "negro", "warmth": 3, "formality": 5, "style": "elegante"},
    {"name": "Tenis Deportivos Negros", "color": "negro", "warmth": 2, "formality": 1, "style": "deportivo"}
]

OUTERWEARS = [
    {"name": "Abrigo Paño Negro", "color": "negro", "warmth": 5, "formality": 5, "style": "elegante"},
    {"name": "Chaqueta de Jean Azul", "color": "azul", "warmth": 3, "formality": 2, "style": "urbano"},
    {"name": "Chaqueta Impermeable Gris", "color": "gris", "warmth": 4, "formality": 2, "style": "casual"},
    {"name": "Chaqueta de Cuero Negra", "color": "negro", "warmth": 4, "formality": 3, "style": "urbano"},
    None
]

OCCASIONS = [
    {"key": "trabajo", "label": "Oficina / Trabajo", "target_formality": 4},
    {"key": "casual", "label": "Universidad / Casual", "target_formality": 2},
    {"key": "formal", "label": "Evento Formal", "target_formality": 5},
    {"key": "fiesta", "label": "Fiesta / Noche", "target_formality": 3},
    {"key": "deporte", "label": "Deporte", "target_formality": 1},
    {"key": "cita", "label": "Cita / Salida Especial", "target_formality": 4}
]

WEATHERS = [
    {"key": "frio", "label": "Frío (8°C - 14°C)", "target_warmth": 4},
    {"key": "templado", "label": "Templado (15°C - 21°C)", "target_warmth": 3},
    {"key": "calido", "label": "Cálido (22°C - 30°C)", "target_warmth": 1},
    {"key": "lluvioso", "label": "Lluvioso / Húmedo", "target_warmth": 5}
]

SYSTEM_PROMPT = "Eres StyleAI, un asistente experto en estilismo, teoría del color y recomendación inteligente de vestuario. Tu objetivo es analizar el armario disponible del usuario y su contexto (clima y ocasión) para seleccionar la mejor combinación de outfits (prenda superior, inferior, calzado y abrigo opcional) calculando un puntaje de match (%) y justificando la decisión de forma clara y lógica."

def evaluate_combination(top, bottom, shoes, outerwear, occasion, weather):
    items = [top, bottom, shoes]
    if outerwear:
        items.append(outerwear)
    
    # 1. Formality score
    avg_formality = sum(i["formality"] for i in items) / len(items)
    formality_diff = abs(avg_formality - occasion["target_formality"])
    formality_score = max(0, 100 - formality_diff * 25)
    
    # 2. Warmth score
    avg_warmth = sum(i["warmth"] for i in items) / len(items)
    warmth_diff = abs(avg_warmth - weather["target_warmth"])
    warmth_score = max(0, 100 - warmth_diff * 25)
    
    # 3. Color score (neutrals boost score)
    neutrals = ["blanco", "negro", "gris", "beige"]
    colors = [i["color"] for i in items]
    neutral_count = sum(1 for c in colors if c in neutrals)
    color_score = 80 + (neutral_count * 5)
    color_score = min(100, color_score)
    
    total_score = round(formality_score * 0.35 + warmth_score * 0.35 + color_score * 0.30)
    total_score = min(99, max(65, total_score))
    
    # Reasoning construction
    reasons = []
    if formality_diff <= 1.0:
        reasons.append(f"Cumple adecuadamente el nivel de formalidad ({round(avg_formality, 1)}/5) para {occasion['label']}.")
    else:
        reasons.append(f"Adaptado para {occasion['label']} equilibrando las prendas disponibles.")
        
    if warmth_diff <= 1.0:
        reasons.append(f"Proporciona la protección térmica necesaria para clima {weather['label']}.")
    else:
        reasons.append(f"Ajusta el abrigo térmico al clima {weather['label']}.")
        
    if neutral_count >= 2:
        reasons.append("Buena paleta de colores usando tonos neutros armoniosos.")
        
    reasoning_text = " ".join(reasons)
    return total_score, reasoning_text

def generate_dataset(num_samples=600, output_path="data/styleai_dataset.jsonl"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    samples = []
    
    for i in range(num_samples):
        # Sample subset of wardrobe for user
        num_tops = random.randint(2, 4)
        num_bottoms = random.randint(2, 3)
        num_shoes = random.randint(2, 3)
        num_outerwears = random.randint(1, 2)
        
        user_tops = random.sample(TOPS, num_tops)
        user_bottoms = random.sample(BOTTOMS, num_bottoms)
        user_shoes = random.sample(SHOES, num_shoes)
        user_outerwears = random.sample(OUTERWEARS, num_outerwears)
        
        occasion = random.choice(OCCASIONS)
        weather = random.choice(WEATHERS)
        
        # Evaluate combinations to find best outfit
        best_combo = None
        best_score = -1
        best_reason = ""
        
        for t in user_tops:
            for b in user_bottoms:
                for s in user_shoes:
                    for o in user_outerwears:
                        score, reason = evaluate_combination(t, b, s, o, occasion, weather)
                        if score > best_score:
                            best_score = score
                            best_combo = (t, b, s, o)
                            best_reason = reason
                            
        top_item, bottom_item, shoes_item, outer_item = best_combo
        
        # Format user prompt
        wardrobe_desc = "Armario del Usuario:\n"
        wardrobe_desc += "- Prenda Superior:\n" + "\n".join([f"  * {x['name']} (Color: {x['color']}, Abrigo: {x['warmth']}/5, Formalidad: {x['formality']}/5)" for x in user_tops]) + "\n"
        wardrobe_desc += "- Prenda Inferior:\n" + "\n".join([f"  * {x['name']} (Color: {x['color']}, Abrigo: {x['warmth']}/5, Formalidad: {x['formality']}/5)" for x in user_bottoms]) + "\n"
        wardrobe_desc += "- Calzado:\n" + "\n".join([f"  * {x['name']} (Color: {x['color']}, Abrigo: {x['warmth']}/5, Formalidad: {x['formality']}/5)" for x in user_shoes]) + "\n"
        valid_outers = [x for x in user_outerwears if x is not None]
        if valid_outers:
            wardrobe_desc += "- Abrigos:\n" + "\n".join([f"  * {x['name']} (Color: {x['color']}, Abrigo: {x['warmth']}/5, Formalidad: {x['formality']}/5)" for x in valid_outers]) + "\n"
            
        context_desc = f"Contexto:\n- Ocasión: {occasion['label']}\n- Clima: {weather['label']}\n"
        
        user_text = f"Por favor recomienda el mejor outfit con las prendas de mi armario para el siguiente contexto:\n\n{wardrobe_desc}\n{context_desc}"
        
        # Assistant response format
        outer_str = f"\n- Abrigo: {outer_item['name']}" if outer_item else ""
        assistant_text = f"**Outfit Recomendado (Match: {best_score}%):**\n- Prenda Superior: {top_item['name']}\n- Prenda Inferior: {bottom_item['name']}\n- Calzado: {shoes_item['name']}{outer_str}\n\n**Justificación:**\n{best_reason}"
        
        sample = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": assistant_text}
            ]
        }
        samples.append(sample)
        
    with open(output_path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            
    print(f"Dataset generado exitosamente con {len(samples)} ejemplos en: {output_path}")

if __name__ == "__main__":
    generate_dataset()
