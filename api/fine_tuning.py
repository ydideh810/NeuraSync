from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from api.checkpointing import save_checkpoint, recover_from_failure
import torch
import time
import random

# Model and dataset paths
MODEL_NAME = "./models/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"
DATASET_PATH = "./pile-train-00001-of-00496.json"

# Fine-tuning function with checkpointing
def distributed_fine_tune(task_id, epochs=3, batch_size=4):
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

    # Restore from checkpoint if exists
    try:
        model = recover_from_failure(task_id, model)
    except FileNotFoundError:
        print("No previous checkpoint found. Starting fresh.")

    # Dataset
    dataset = load_dataset("json", data_files=DATASET_PATH)["train"]

    # LoRA fine-tuning config
    lora_config = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.1, target_modules=["q_proj", "v_proj"])
    model = get_peft_model(model, lora_config)

    # Training configuration
    training_args = TrainingArguments(
        output_dir="./fine-tuned-model",
        evaluation_strategy="epoch",
        learning_rate=1e-4,
        per_device_train_batch_size=batch_size,
        num_train_epochs=epochs,
        logging_dir="./logs",
        save_steps=100  # Save checkpoint every 100 steps
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=dataset)

    # Fine-tuning loop with periodic checkpointing
    for epoch in range(epochs):
        trainer.train()

        # Save checkpoint
        checkpoint_path = save_checkpoint(model, task_id)
        print(f"Checkpoint saved at {checkpoint_path}")

    return {"task_id": task_id, "status": "completed"}
