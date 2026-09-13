import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_PATH = "./styleai-llm-adapter"

def generate_recommendation(user_prompt: str, use_adapter: bool = True):
    print("Cargando modelo para inferencia...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True
    )

    if use_adapter and torch.os.path.exists(ADAPTER_PATH):
        print(f"Cargando adaptadores fine-tuneados desde {ADAPTER_PATH}...")
        model = PeftModel.from_pretrained(model, ADAPTER_PATH)

    messages = [
        {"role": "system", "content": "Eres StyleAI, un asistente experto en recomendación inteligente de vestuario. Analiza el armario del usuario y su contexto (clima y ocasión) para seleccionar la mejor combinación de outfits calculando un puntaje de match (%) y justificando la decisión de forma clara y lógica."},
        {"role": "user", "content": user_prompt}
    ]

    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([prompt], return_tensors="pt")

    print("\nGenerando recomendación de outfit...\n")
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        top_p=0.9
    )

    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    test_prompt = """Por favor recomienda el mejor outfit con las prendas de mi armario:

Armario del Usuario:
- Prenda Superior:
  * Camisa Oxford Blanca (Color: blanco, Abrigo: 2/5, Formalidad: 4/5)
  * Camiseta Negra Básica (Color: negro, Abrigo: 1/5, Formalidad: 1/5)
- Prenda Inferior:
  * Pantalón de Vestir Negro (Color: negro, Abrigo: 3/5, Formalidad: 5/5)
  * Jeans Azules Oscuros (Color: azul, Abrigo: 3/5, Formalidad: 2/5)
- Calzado:
  * Zapatos de Cuero Café (Color: cafe, Abrigo: 3/5, Formalidad: 5/5)
  * Tenis Blancos Urbano (Color: blanco, Abrigo: 2/5, Formalidad: 1/5)
- Abrigos:
  * Abrigo Paño Negro (Color: negro, Abrigo: 5/5, Formalidad: 5/5)

Contexto:
- Ocasión: Oficina / Trabajo
- Clima: Frío (8°C - 14°C)
"""
    result = generate_recommendation(test_prompt, use_adapter=False)
    print("=== Resultado de Inferencia StyleAI ===")
    print(result)

