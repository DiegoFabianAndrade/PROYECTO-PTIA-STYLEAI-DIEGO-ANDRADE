"""
train_styleai_llm.py
--------------------
Script de entrenamiento (Fine-Tuning) para el proyecto StyleAI usando Hugging Face PEFT / QLoRA.
Entrena un LLM (ej. Qwen/Qwen2.5-1.5B-Instruct, meta-llama/Llama-3.2-1B-Instruct o TinyLlama/TinyLlama-1.1B-Chat-v1.0)
utilizando cuantización de 4-bits y adaptadores LoRA.
"""

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
from trl import SFTTrainer

# --- CONFIGURACIÓN DE PARÁMETROS ---
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"  # O "meta-llama/Llama-3.2-1B-Instruct" / "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATASET_PATH = "data/styleai_dataset.jsonl"
OUTPUT_DIR = "./styleai-llm-adapter"
LOGGING_DIR = "./logs"

def main():
    print(f"=== Iniciando Pipeline de Fine-Tuning StyleAI con {MODEL_NAME} ===")
    
    # 1. Cargar Dataset
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"No se encontró el dataset en {DATASET_PATH}. Ejecuta dataset_generator.py primero.")
        
    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")
    print(f"Dataset cargado correctamente con {len(dataset)} muestras.")

    # 2. Configurar Cuantización a 4-Bits (QLoRA)
    use_cuda = torch.cuda.is_available()
    print(f"CUDA disponible: {use_cuda}")
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16 if use_cuda else torch.float32,
        bnb_4bit_use_double_quant=True
    ) if use_cuda else None

    # 3. Cargar Tokenizer y Modelo Base
    print("Cargando tokenizer y modelo base...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto" if use_cuda else None,
        trust_remote_code=True,
        torch_dtype=torch.float16 if use_cuda else torch.float32
    )

    if use_cuda:
        model = prepare_model_for_kbit_training(model)

    # 4. Configuración de Adaptadores LoRA (PEFT)
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 5. Configurar Hiperparámetros de Entrenamiento
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        max_steps=100,  # Cambiar por num_train_epochs=3 para entrenamiento completo
        learning_rate=2e-4,
        fp16=use_cuda,
        logging_steps=10,
        save_strategy="steps",
        save_steps=50,
        optim="adamw_torch",
        report_to="none"
    )

    # 6. Inicializar SFTTrainer (Supervised Fine-Tuning)
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="messages",
        max_seq_length=512,
        tokenizer=tokenizer,
        args=training_args,
    )

    # 7. Ejecutar Fine-Tuning y Guardar Adaptadores
    print("Iniciando entrenamiento...")
    trainer.train()

    print(f"Entrenamiento finalizado. Guardando adaptador fine-tuneado en {OUTPUT_DIR}...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("¡Fine-Tuning completado exitosamente para StyleAI!")

if __name__ == "__main__":
    main()
