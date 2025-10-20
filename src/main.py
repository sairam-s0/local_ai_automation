"""
Screen AI Assistant - Main Application
Combines screenshot capture + AI processing
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from pathlib import Path
import keyboard
from PIL import ImageGrab, ImageTk, Image
import time
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our modules (try both ways)
try:
    from solver_ai import FastAISolver
    from scr import ScreenshotOverlay
except ImportError:
    # If running from parent directory
    from src.solver_ai import FastAISolver
    from src.scr import ScreenshotOverlay


class ScreenAIApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen AI Assistant 🤖")
        self.root.geometry("800x600")
        
        # Initialize components
        self.solver = FastAISolver()  # No parameters needed
        self.overlay = ScreenshotOverlay()
        self.current_screenshot = None
        
        # Setup UI
        self.setup_ui()
        
        # Setup hotkey
        keyboard.add_hotkey('ctrl+shift+s', self.trigger_capture)
        
        # Create folders
        Path("screenshots").mkdir(exist_ok=True)
    
    def setup_ui(self):
        """Setup the main UI"""
        # Title
        title = tk.Label(
            self.root,
            text="📸 Screen AI Assistant",
            font=("Arial", 20, "bold"),
            bg="#4A90E2",
            fg="white",
            pady=15
        )
        title.pack(fill=tk.X)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Capture button
        capture_btn = tk.Button(
            left_panel,
            text="📸 Capture Screen\n(Ctrl+Shift+S)",
            font=("Arial", 12, "bold"),
            bg="#4A90E2",
            fg="white",
            activebackground="#357ABD",
            command=self.check_and_process,  # Changed to auto-process
            height=3,
            cursor="hand2"
        )
        capture_btn.pack(fill=tk.X, pady=5)
        
        # Process last button
        process_btn = tk.Button(
            left_panel,
            text="🤖 Process Last",
            font=("Arial", 11),
            bg="#5CB85C",
            fg="white",
            command=self.process_last_screenshot,
            cursor="hand2"
        )
        process_btn.pack(fill=tk.X, pady=5)
        
        # Batch process button
        batch_btn = tk.Button(
            left_panel,
            text="📚 Batch Process",
            font=("Arial", 11),
            bg="#F0AD4E",
            fg="white",
            command=self.batch_process,
            cursor="hand2"
        )
        batch_btn.pack(fill=tk.X, pady=5)
        
        # Settings
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        settings_label = tk.Label(left_panel, text="⚙️ Settings", font=("Arial", 12, "bold"))
        settings_label.pack(pady=5)
        
        # Auto-process toggle
        self.auto_process_var = tk.BooleanVar(value=True)  # Default ON for speed!
        auto_check = ttk.Checkbutton(
            left_panel,
            text="Auto-process captures",
            variable=self.auto_process_var
        )
        auto_check.pack(anchor=tk.W, pady=2)
        
        # Stats
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        stats_label = tk.Label(left_panel, text="📊 Stats", font=("Arial", 12, "bold"))
        stats_label.pack(pady=5)
        
        self.stats_text = tk.Label(
            left_panel,
            text="Screenshots: 0\nProcessed: 0",
            font=("Arial", 10),
            justify=tk.LEFT
        )
        self.stats_text.pack(anchor=tk.W)
        
        # Right panel - Results
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Results label
        results_label = tk.Label(right_panel, text="🤖 AI Response", font=("Arial", 14, "bold"))
        results_label.pack(pady=(0, 10))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#F5F5F5"
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#E0E0E0"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def trigger_capture(self):
        """Trigger screenshot capture"""
        self.status_var.set("📸 Capturing screen...")
        
        def capture():
            # Create new overlay instance
            overlay = ScreenshotOverlay()
            overlay.start_capture()
            
            # After capture completes, process if auto-process is enabled
            self.root.after(1000, self.check_and_process)
        
        threading.Thread(target=capture, daemon=True).start()
    
    def check_and_process(self):
        """Check for new screenshot and process if auto-process enabled"""
        if self.auto_process_var.get():
            # Small delay to ensure file is saved
            self.root.after(500, self.process_last_screenshot)
        
        self.update_stats()
    
    def process_last_screenshot(self):
        """Process the most recent screenshot"""
        screenshots = sorted(Path("screenshots").glob("*.png"))
        
        if not screenshots:
            messagebox.showwarning("No Screenshots", "Capture a screenshot first!")
            return
        
        latest = screenshots[-1]
        self.current_screenshot = latest
        
        self.status_var.set(f"🤖 Processing {latest.name}...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, "⏳ Processing with AI...\n\n")
        
        def process():
            result = self.solver.solve(latest)
            
            self.root.after(0, lambda: self.display_result(result, latest.name))
        
        threading.Thread(target=process, daemon=True).start()
    
    def batch_process(self):
        """Process all screenshots in batch"""
        screenshots = list(Path("screenshots").glob("*.png"))
        
        if not screenshots:
            messagebox.showwarning("No Screenshots", "No screenshots to process!")
            return
        
        if not messagebox.askyesno("Batch Process", 
                                   f"Process {len(screenshots)} screenshots?"):
            return
        
        self.status_var.set(f"🔄 Batch processing {len(screenshots)} images...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, f"⏳ Processing {len(screenshots)} images...\n\n")
        
        def batch():
            results = self.solver.batch_solve("screenshots", "fast_answers.txt")
            self.root.after(0, lambda: self.batch_complete(len(results)))
        
        threading.Thread(target=batch, daemon=True).start()
    
    def batch_complete(self, count):
        """Called when batch processing completes"""
        self.status_var.set(f"✅ Batch complete! Processed {count} images")
        self.results_text.insert(tk.END, f"\n✅ Complete! Check fast_answers.txt")
        messagebox.showinfo("Complete", f"Processed {count} images!\n\nResults in fast_answers.txt")
    
    def display_result(self, result, filename):
        """Display AI result"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, f"📸 {filename}\n\n")
        self.results_text.insert(tk.END, result)
        
        self.status_var.set(f"✅ Processed {filename}")
        self.update_stats()
    
    def update_stats(self):
        """Update statistics"""
        screenshots = len(list(Path("screenshots").glob("*.png")))
        # Count processed by checking answers file
        processed = 0
        if Path("fast_answers.txt").exists():
            with open("fast_answers.txt", "r", encoding="utf-8") as f:
                processed = f.read().count("[")
        
        self.stats_text.config(text=f"Screenshots: {screenshots}\nProcessed: {processed}")
    
    def run(self):
        """Run the application"""
        print("\n🚀 Screen AI Assistant Started!")
        print("📌 Use Ctrl+Shift+S to capture anywhere")
        print("🪟 Main window opened\n")
        
        self.root.mainloop()


if __name__ == "__main__":
    app = ScreenAIApp()
    app.run()