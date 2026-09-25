import os
import sys

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
except ImportError:
    print("Error: transformers library not found.")
    sys.exit(1)

def download_model():
    model_name = "facebook/nllb-200-distilled-600M"
    print(f"Downloading model {model_name}...")
    print("This is a ~1.2GB model. Please wait...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print("Download complete! The model has been cached successfully.")
    
if __name__ == '__main__':
    download_model()
