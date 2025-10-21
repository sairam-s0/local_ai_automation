import ollama
import easyocr
from pathlib import Path
import time

class FastAISolver:
    def __init__(self):
        print("🚀 Initializing Fast AI Solver...")
        print("📝 Loading EasyOCR (first time is slow)...")
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.model = 'phi3'
        self.base_dir = Path(__file__).resolve().parent
        print(f"✅ Ready!")
    
    def extract_text(self, image_path):
        try:
            result = self.reader.readtext(str(image_path), detail=0)
            return " ".join(result)
        except Exception as e:
            print(f"❌ OCR error: {e}")
            return ""
    
    def answer_question(self, text):
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': f"Answer this question concisely:\n\n{text}"}],
                options={'num_predict': 200}
            )
            return response['message']['content']
        except Exception as e:
            return f"AI Error: {e}"
    
    def solve(self, image_path):
        image_path = Path(image_path)
        print(f"\n📸 Processing: {image_path.name}")
        
        text = self.extract_text(image_path)
        if not text:
            return "⚠️ No text found"
        
        print(f"📝 Extracted: {text[:100]}...")
        answer = self.answer_question(text)
        
        # Save with clear delimiter
        answers_file = self.base_dir / "fast_answers.txt"
        with open(answers_file, "a", encoding="utf-8") as f:
            f.write(f"\n=== ANSWER START ===\n")
            f.write(f"File: {image_path.name}\n")
            f.write(f"Text: {text}\n")
            f.write(f"Answer: {answer}\n")
            f.write(f"=== ANSWER END ===\n")
        
        return f"TEXT:\n{text}\n\nANSWER:\n{answer}"