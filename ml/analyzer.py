import spacy
from spacy.util import is_package
from spacy.cli import download
  
# Risky phrases/clauses
RISKY_PHRASES = [
  "indemnify", "hold harmless", "liquidated damages", "termination", "arbitration", "non-disclosure",
  "penalty", "unilateral", "binding", "force majeure", "warranty", "liability", "exclusive", "governing law"
]

def ensure_model(model_name):
  if not is_package(model_name):
    try:
      download(model_name)
    except Exception as e:
      print(f"Failed to download {model_name}: {e}")
      
# Load spaCy large or small English legal model
try:
  model = "en_core_web_lg"
  ensure_model(model)
  nlp = spacy.load(model)
except:
  model = "en_core_web_sm"
  ensure_model(model)
  nlp = spacy.load(model)

def analyze_document(text):
  doc = nlp(text)
  highlights = []
  risk_score = 0
  for sent in doc.sents:
    for phrase in RISKY_PHRASES:
      if phrase in sent.text.lower():
        highlights.append(sent.text)
        risk_score += 1
  risk_score = min(1.0, risk_score / 12.0) # Normalize risk
  return {
      'risk_score': round(risk_score * 100, 1),
      'highlights': highlights
    }