"""
AI Solver - SUPER FAST VERSION with Tesseract + Phi-3
Minimal dependencies, maximum speed!
"""

import ollama
import pytesseract
from PIL import Image
from pathlib import Path
import time

class FastAISolver:
    def __init__(self):
        print("🚀 Initializing Fast AI Solver...")
        
        # Use Phi-3 for answering
        self.model = 'phi3'
        
        print(f"✅ Ready! Using Tesseract OCR + {self.model}")
    
    def extract_text(self, image_path):
        """Extract text from image using Tesseract (INSTANT!)"""
        try:
            # Run OCR
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            
            return text.strip()
            
        except Exception as e:
            print(f"❌ OCR error: {e}")
            return ""
    
    def answer_question(self, text):
        """Use Phi-3 to answer the question"""
        try:
            prompt = f"""You are a quick quiz assistant. Analyze this question and provide a concise answer.

Question/Text:
{text}

Instructions:
1. If it's a multiple choice question, identify the correct answer(s)
2. Provide a brief explanation (2-3 sentences max)
3. Be direct and fast

Answer:"""

            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.3,  # More focused
                    'num_predict': 200   # Shorter responses = faster
                }
            )
            
            return response['message']['content']
            
        except Exception as e:
            print(f"❌ AI error: {e}")
            return "Error processing question"
    
    def solve(self, image_path):
        """Main solve method - FAST pipeline"""
        image_path = Path(image_path)
        
        if not image_path.exists():
            return f"❌ Image not found: {image_path}"
        
        print(f"\n{'='*60}")
        print(f"📸 Processing: {image_path.name}")
        
        # Step 1: Extract text (FAST with PaddleOCR)
        start = time.time()
        print("📝 Extracting text with PaddleOCR...")
        text = self.extract_text(image_path)
        ocr_time = time.time() - start
        
        if not text.strip():
            return "⚠️ No text found in image"
        
        print(f"✅ Extracted text in {ocr_time:.2f}s")
        print(f"📄 Text preview: {text[:150]}...")
        
        # Step 2: Get answer from Phi-3 (FAST)
        start = time.time()
        print(f"🤖 Getting answer from {self.model}...")
        answer = self.answer_question(text)
        ai_time = time.time() - start
        
        print(f"✅ Answer generated in {ai_time:.2f}s")
        print(f"⚡ Total time: {ocr_time + ai_time:.2f}s")
        print(f"{'='*60}\n")
        
        # Format result
        result = f"""📝 EXTRACTED TEXT:
{text}

{'='*60}

🤖 AI ANSWER:
{answer}

{'='*60}
⏱️ Processing time: {ocr_time + ai_time:.2f}s (OCR: {ocr_time:.2f}s, AI: {ai_time:.2f}s)
"""
        
        return result
    
    def batch_solve(self, image_folder, output_file="fast_answers.txt"):
        """Process multiple screenshots quickly"""
        folder = Path(image_folder)
        images = sorted(folder.glob("*.png"))
        
        if not images:
            print(f"⚠️ No PNG images found in {folder}")
            return
        
        print(f"\n🚀 FAST Batch processing {len(images)} images...\n")
        
        total_start = time.time()
        results = []
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"{'='*60}\n")
            f.write(f"FAST AI SOLVER - Batch Results\n")
            f.write(f"Total images: {len(images)}\n")
            f.write(f"{'='*60}\n\n")
        
        for i, img_path in enumerate(images, 1):
            print(f"[{i}/{len(images)}] Processing {img_path.name}...")
            
            result = self.solve(img_path)
            
            results.append({
                'image': img_path.name,
                'answer': result,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Save incrementally
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"[{i}/{len(images)}] {img_path.name}\n")
                f.write(f"Time: {results[-1]['timestamp']}\n")
                f.write(f"{'='*60}\n\n")
                f.write(result)
                f.write("\n\n")
            
            print(f"✅ Saved to {output_file}\n")
        
        total_time = time.time() - total_start
        avg_time = total_time / len(images)
        
        summary = f"""
{'='*60}
🎉 BATCH COMPLETE!
{'='*60}
Total images: {len(images)}
Total time: {total_time:.2f}s
Average time per image: {avg_time:.2f}s
Speed: {len(images)/total_time*60:.1f} images/minute
{'='*60}
"""
        
        print(summary)
        
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(summary)
        
        print(f"📄 All results saved to: {output_file}")
        
        return results


def test_solver():
    """Test the fast solver"""
    solver = FastAISolver()
    
    # Check for test images
    screenshots = Path("screenshots")
    if screenshots.exists():
        images = list(screenshots.glob("*.png"))
        if images:
            print("\n📸 Testing with latest screenshot...")
            result = solver.solve(images[-1])
            print(f"\n{result}")
        else:
            print("⚠️ No screenshots found. Capture one first!")
    else:
        print("⚠️ Screenshots folder not found")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--batch":
            # Batch mode
            solver = FastAISolver()
            solver.batch_solve("screenshots")
        else:
            # Process specific image
            solver = FastAISolver()
            result = solver.solve(sys.argv[1])
            print(f"\n{result}")
    else:
        # Test mode
        test_solver()