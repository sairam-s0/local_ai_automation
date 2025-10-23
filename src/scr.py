

import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, Image, ImageTk
import keyboard
import threading
import time
from pathlib import Path

class ScreenshotOverlay:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = None
        self.canvas = None
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.screenshot = None
        self.is_active = False
        self.last_saved_path = None
        
        # Create screenshots folder relative to script
        self.base_dir = Path(__file__).resolve().parent
        self.screenshots_dir = self.base_dir / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
        
    def start_capture(self):
        """Initialize the overlay for screenshot capture"""
        if self.is_active:
            return None
            
        self.is_active = True
        
        # Take screenshot before creating overlay
        self.screenshot = ImageGrab.grab()
        
        # Create fullscreen transparent window
        self.root = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            cursor="cross",
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.cancel())
        
        # Instructions
        label = tk.Label(
            self.root,
            text="📸 Drag to select area • ESC to cancel",
            font=("Arial", 14),
            fg="white",
            bg="black"
        )
        label.place(relx=0.5, rely=0.02, anchor="n")
        
        # Make modal
        self.root.grab_set()
        self.root.wait_window(self.root)
        
        return self.last_saved_path

    def on_press(self, event):
        """Mouse press - start selection"""
        self.start_x = event.x
        self.start_y = event.y
        
        # Create rectangle
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=3
        )
    
    def on_drag(self, event):
        """Mouse drag - update selection"""
        if self.rect:
            self.canvas.coords(
                self.rect,
                self.start_x, self.start_y,
                event.x, event.y
            )
    
    def on_release(self, event):
        """Mouse release - capture selected area"""
        if not self.rect:
            return
        
        # Get coordinates
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        # Crop screenshot
        cropped = self.screenshot.crop((x1, y1, x2, y2))
        
        # Save with timestamp using absolute path
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = self.screenshots_dir / f"capture_{timestamp}.png"
        cropped.save(filepath)
        
        self.last_saved_path = str(filepath)
        print(f"\n✅ Screenshot saved: {filepath}")
        
        # Close overlay
        self.cleanup()
        
        # Return filepath for processing
        return filepath
    
    def cancel(self):
        """Cancel capture"""
        print("\n❌ Capture cancelled")
        self.cleanup()
    
    def cleanup(self):
        """Clean up and close overlay"""
        self.is_active = False
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None


class FloatingButton:
    """Floating button that hovers on screen"""
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Tk()
        self.root.title("Screen AI")
        
        # Make it float
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-alpha', 0.9)
        
        # Position in top-right corner
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"120x60+{screen_width-140}+20")
        
        # Style
        self.root.configure(bg='#4A90E2')
        
        # Button
        btn = tk.Button(
            self.root,
            text="📸 Capture\n(Ctrl+Shift+S)",
            font=("Arial", 10, "bold"),
            bg='#4A90E2',
            fg='white',
            activebackground='#357ABD',
            activeforeground='white',
            border=0,
            command=self.trigger_capture,
            cursor="hand2"
        )
        btn.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Make draggable
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)
        btn.bind('<Button-1>', self.start_move)
        btn.bind('<B1-Motion>', self.on_move)
        
        self.x = 0
        self.y = 0
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def trigger_capture(self):
        """Trigger screenshot capture"""
        self.callback()
    
    def run(self):
        self.root.mainloop()


def main():

    overlay = ScreenshotOverlay()
    
    def capture_hotkey():
        
        print("\n🎯 Screenshot mode activated!")
        threading.Thread(target=overlay.start_capture, daemon=True).start()
    
    # Register global hotkey
    keyboard.add_hotkey('ctrl+shift+s', capture_hotkey)
    
    print("🚀 Screen AI Assistant Started!")
    print("📌 Floating button will appear on screen")
    print("⌨️  Hotkey: Ctrl+Shift+S to capture")
    print("❌ Press Ctrl+C to exit\n")
    
    # Start floating button
    floating_btn = FloatingButton(capture_hotkey)
    
    try:
        floating_btn.run()
    except KeyboardInterrupt:
        print("\n\n👋 Screen AI stopped")


if __name__ == "__main__":
    main()
