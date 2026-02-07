import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Python Calculator")
        self.root.geometry("380x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")  # Dark theme background

        self.equation = ""
        
        # Display screens
        self.display_frame = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        self.display_frame.pack(expand=True, fill="both")

        # Previous expression label
        self.prev_label = tk.Label(
            self.display_frame, 
            text="", 
            anchor="e", 
            bg="#1e1e2e", 
            fg="#6c7086", 
            font=("Inter", 12),
            padx=20
        )
        self.prev_label.pack(fill="x")

        # Main display label
        self.display_label = tk.Label(
            self.display_frame, 
            text="0", 
            anchor="e", 
            bg="#1e1e2e", 
            fg="#cdd6f4", 
            font=("Inter", 36, "bold"),
            padx=20
        )
        self.display_label.pack(fill="x")

        # Buttons frame
        self.buttons_frame = tk.Frame(self.root, bg="#1e1e2e", padx=10, pady=10)
        self.buttons_frame.pack(expand=True, fill="both")

        # Button groups configuration
        # Colors: Numbers (#313244), Operators (#89b4fa), Special (#f38ba8), Equals (#a6e3a1)
        buttons = [
            ('C', 0, 0, "#f38ba8"), ('DEL', 0, 1, "#fab387"), ('%', 0, 2, "#89b4fa"), ('/', 0, 3, "#89b4fa"),
            ('7', 1, 0, "#313244"), ('8', 1, 1, "#313244"), ('9', 1, 2, "#313244"), ('*', 1, 3, "#89b4fa"),
            ('4', 2, 0, "#313244"), ('5', 2, 1, "#313244"), ('6', 2, 2, "#313244"), ('-', 2, 3, "#89b4fa"),
            ('1', 3, 0, "#313244"), ('2', 3, 1, "#313244"), ('3', 3, 2, "#313244"), ('+', 3, 3, "#89b4fa"),
            ('0', 4, 0, "#313244", 2), ('.', 4, 2, "#313244"), ('=', 4, 3, "#a6e3a1")
        ]

        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            color = btn[3]
            colspan = btn[4] if len(btn) > 4 else 1
            
            self.create_button(text, row, col, color, colspan)

        # Bind keyboard
        self.root.bind('<Key>', self.key_event)

    def create_button(self, text, row, col, bg_color, colspan=1):
        button = tk.Button(
            self.buttons_frame,
            text=text,
            font=("Inter", 14, "bold"),
            bg=bg_color,
            fg="#11111b" if bg_color in ["#a6e3a1", "#89b4fa", "#fab387", "#f38ba8"] else "#cdd6f4",
            borderwidth=0,
            activebackground="#45475a",
            activeforeground="white",
            cursor="hand2",
            command=lambda t=text: self.on_button_click(t)
        )
        button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)
        
        # Configure weights for responsive grid
        self.buttons_frame.grid_columnconfigure(col, weight=1)
        self.buttons_frame.grid_rowconfigure(row, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.equation = ""
            self.prev_label.config(text="")
        elif char == 'DEL':
            self.equation = self.equation[:-1]
        elif char == '=':
            self.calculate()
            return
        else:
            # Prevent leading zeros unless it's a decimal
            if self.equation == "0" and char.isdigit():
                self.equation = char
            else:
                self.equation += str(char)
        
        self.update_display()

    def calculate(self):
        try:
            expression = self.equation.replace('×', '*').replace('÷', '/').replace('%', '/100')
            
            # Пасхалка: 2+2 = 5
            if expression == "2+2":
                result = "5"
            else:
                result = str(eval(expression))
            
            self.prev_label.config(text=f"{self.equation} =")
            self.equation = result
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero!")
            self.equation = ""
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.equation = ""
        
        self.update_display()

    def update_display(self):
        display_text = self.equation if self.equation else "0"
        # Limit display length
        if len(display_text) > 15:
            display_text = display_text[:12] + "..."
        self.display_label.config(text=display_text)

    def key_event(self, event):
        key = event.char
        if key in "0123456789.+-*/%":
            self.on_button_click(key)
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.on_button_click('DEL')
        elif event.keysym == "Escape":
            self.on_button_click('C')

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
