import spacy

# Load spaCy legal model or English
try:
  nlp = spacy.load("en_core_web_lg")
except:
  nlp = spacy.load("en_core_web_sm")
  
# Risky phrases/clauses
RISKY_PHRASES = [
  "indemnify", "hold harmless", "liquidated damages", "termination", "arbitration", "non-disclosure",
  "penalty", "unilateral", "binding", "force majeure", "warranty", "liability", "exclusive", "governing law"
]

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