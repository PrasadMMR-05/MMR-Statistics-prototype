from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load model once
MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def generate_answer(prompt: str) -> str:
    """
    Generates answer text from prompt using Flan-T5.
    """

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.3
        )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text
