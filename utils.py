from keybert import KeyBERT
import spacy

nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_keywords(text, top_n=5):
    keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
    return [kw[0] for kw in keywords]

def clean_text(text):
    doc = nlp(text)
    return " ".join([sent.text.strip() for sent in doc.sents if len(sent.text.split()) > 5])
