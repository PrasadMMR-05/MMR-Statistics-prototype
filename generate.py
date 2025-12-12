from transformers import T5ForConditionalGeneration, T5Tokenizer

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

def build_prompt(query, stats):
    context = ""
    for s in stats:
        context += f"{s['statisticId']} | {s['title']}\n"

    prompt = f"""
You are an analyst. Use the context below (each entry is a statistic).
For each bullet, append the STAT_ID in brackets like [STAT_ID].
Do not invent numbers.

Context:
{context}

Question: {query}

Answer in 5 bullets. Then list Sources:
"""
    return prompt.strip()

def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    output = model.generate(**inputs, max_length=300)
    return tokenizer.decode(output[0], skip_special_tokens=True)
