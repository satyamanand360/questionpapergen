from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random

# Load model
tokenizer = AutoTokenizer.from_pretrained("valhalla/t5-base-qg-hl")
model = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-base-qg-hl")

def generate_question(context, answer):
    prompt = f"generate question: {context} answer: {answer}"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def generate_fill_in_blank(context, keyword):
    sentence = context.replace(keyword, "_____")
    return sentence, keyword

def generate_true_false(context, keyword):
    if random.random() < 0.5:
        return f"{keyword} is associated with: {context}", "True"
    else:
        fake = keyword[::-1]
        return f"{fake} is associated with: {context}", "False"

def generate_mcq(context, keyword):
    distractors = [keyword[::-1], keyword.upper(), keyword.lower()]
    options = [keyword] + distractors
    random.shuffle(options)
    question = generate_question(context, keyword)
    return question, options, keyword

def generate_match_columns(keywords):
    col_A = keywords
    col_B = [k[::-1] for k in keywords]
    random.shuffle(col_B)
    return list(zip(col_A, col_B)), dict(zip(col_A, [k[::-1] for k in col_A]))

