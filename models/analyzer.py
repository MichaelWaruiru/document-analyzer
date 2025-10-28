import spacy
from spacy.util import is_package
from spacy.cli import download
  
# Risky phrases/clauses
RISKY_PHRASES = [
  "indemnify", "hold harmless", "liquidated damages", "termination", "arbitration", "non-disclosure",
  "penalty", "unilateral", "binding", "force majeure", "warranty", "liability", "exclusive", "governing law"
]

# Lazy loading
nlp = None

def ensure_model(model_name):
  if not is_package(model_name):
    try:
      download(model_name)
    except Exception as e:
      print(f"Failed to download {model_name}: {e}")

"""Uncomment this and comment the function below this to use the large model"""
# def get_nlp():
#   """Load spaCy large or small English legal model & cache it
#   """
#   global nlp
#   if nlp is None:
#     try:
#       model = "en_core_web_lm" #Uses the large model
#       nlp = spacy.load(model)
#     except:
#       model = "en_core_web_sm"
#       nlp = spacy.blank("en")
#   return nlp

def get_nlp():
    """Lazy loading and cache spaCy model safely."""
    global nlp
    if nlp is None:
        try:
            model = "en_core_web_sm"  # use the small model for Render
            ensure_model(model)
            nlp = spacy.load(model)
            print(f"Loaded spaCy model: {model}")
        except Exception as e:
            print(f"Error loading spaCy model: {e}")
            nlp = spacy.blank("en")
            # Add a simple sentencizer if using a blank model
            if "sentencizer" not in nlp.pipe_names:
                nlp.add_pipe("sentencizer")
                print("Added sentencizer to blank pipeline.")
    else:
        # ensure sentence segmentation exists (for any model)
        if "parser" not in nlp.pipe_names and "senter" not in nlp.pipe_names:
            if "sentencizer" not in nlp.pipe_names:
                nlp.add_pipe("sentencizer")
    return nlp

def analyze_document(text):
  nlp_model = get_nlp() # Load model only once, reuse afterword
  doc = nlp_model(text)
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