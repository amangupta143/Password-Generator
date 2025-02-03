import tkinter as tk
from tkinter import ttk
import string
import random
import json
from pathlib import Path

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x500")
        
        # Variables
        self.password_length = tk.IntVar(value=12)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_numbers = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.password_result = tk.StringVar()
        
        self.setup_ui()
        self.load_preferences()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Length section
        ttk.Label(main_frame, text="Password Length:").grid(row=0, column=0, sticky=tk.W)
        length_spinbox = ttk.Spinbox(
            main_frame, 
            from_=8, 
            to=30, 
            textvariable=self.password_length,
            width=5
        )
        length_spinbox.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Character types
        ttk.Checkbutton(main_frame, text="Uppercase", variable=self.use_uppercase).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(main_frame, text="Lowercase", variable=self.use_lowercase).grid(row=2, column=0, sticky=tk.W)
        ttk.Checkbutton(main_frame, text="Numbers", variable=self.use_numbers).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(main_frame, text="Symbols", variable=self.use_symbols).grid(row=4, column=0, sticky=tk.W)
        
        # Buttons
        ttk.Button(main_frame, text="Generate Password", command=self.generate_password).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Result display
        result_frame = ttk.LabelFrame(main_frame, text="Generated Password", padding="10")
        result_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Entry(result_frame, textvariable=self.password_result, font=('Courier', 12)).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(result_frame, text="Copy", command=self.copy_password).grid(row=0, column=1, padx=5)
        
        # Error message
        self.error_label = ttk.Label(main_frame, foreground='red')
        self.error_label.grid(row=7, column=0, columnspan=2, pady=10)

    def generate_password(self):
        try:
            # Validate selections
            if not any([self.use_uppercase.get(), self.use_lowercase.get(), 
                       self.use_numbers.get(), self.use_symbols.get()]):
                raise ValueError("Select at least one character type")

            # Build character pool
            chars = ''
            if self.use_uppercase.get(): chars += string.ascii_uppercase
            if self.use_lowercase.get(): chars += string.ascii_lowercase
            if self.use_numbers.get(): chars += string.digits
            if self.use_symbols.get(): chars += string.punctuation

            # Generate password
            password = ''.join(random.choice(chars) for _ in range(self.password_length.get()))
            self.password_result.set(password)
            self.error_label.config(text="")
            self.save_preferences()
            
        except ValueError as e:
            self.error_label.config(text=str(e))
    
    def copy_password(self):
        if self.password_result.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.password_result.get())
            self.error_label.config(text="Password copied to clipboard!", foreground='green')
    
    def save_preferences(self):
        prefs = {
            "length": self.password_length.get(),
            "uppercase": self.use_uppercase.get(),
            "lowercase": self.use_lowercase.get(),
            "numbers": self.use_numbers.get(),
            "symbols": self.use_symbols.get()
        }
        Path('preferences.json').write_text(json.dumps(prefs))
    
    def load_preferences(self):
        try:
            if Path('preferences.json').exists():
                prefs = json.loads(Path('preferences.json').read_text())
                self.password_length.set(prefs.get("length", 12))
                self.use_uppercase.set(prefs.get("uppercase", True))
                self.use_lowercase.set(prefs.get("lowercase", True))
                self.use_numbers.set(prefs.get("numbers", True))
                self.use_symbols.set(prefs.get("symbols", True))
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()