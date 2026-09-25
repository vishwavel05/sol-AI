import os

class OfflineTranslator:
    _instance = None
    
    def __init__(self):
        if OfflineTranslator._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            OfflineTranslator._instance = self
            self.model_name = "facebook/nllb-200-distilled-600M"
            self.translator = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    def _load_model(self):
        if self.translator is None:
            print("Loading offline NLLB translator into memory...")
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, src_lang="tam_Taml")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.translator = True

    def translate(self, text: str) -> str:
        if not text or not str(text).strip():
            return ""
        self._load_model()
        try:
            inputs = self.tokenizer(text, return_tensors="pt")
            translated_tokens = self.model.generate(
                **inputs, forced_bos_token_id=self.tokenizer.lang_code_to_id["eng_Latn"], max_length=400
            )
            translated = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
            # NLLB sometimes hallucinates other languages (Chinese, Telugu). Force it to English-like text
            # by removing characters outside basic Latin/ASCII.
            import re
            cleaned = re.sub(r'[^\x00-\x7F]+', '', translated).strip()
            return cleaned
        except Exception as e:
            print(f"[Offline Translator Error] {e}")
            return ""
