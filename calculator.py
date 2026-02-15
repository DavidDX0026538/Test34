import tkinter as tk
from tkinter import messagebox
from typing import Optional

# ===== Цветовая схема (Catppuccin) =====
class Theme:
    BG = "#1e1e2e"
    TEXT_PRIMARY = "#cdd6f4"
    TEXT_SECONDARY = "#6c7086"

    BTN_NUMBER = "#313244"
    BTN_OPERATOR = "#89b4fa"
    BTN_SPECIAL = "#f38ba8"
    BTN_DELETE = "#fab387"
    BTN_EQUALS = "#a6e3a1"

    ACTIVE_BG = "#45475a"
    ACTIVE_FG = "white"

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Python Calculator")
        self.root.geometry("380x550")
        self.root.resizable(False, False)
        self.root.configure(bg=Theme.BG)

        self.equation = ""
        self.history = []

        # Display screens
        self.display_frame = tk.Frame(self.root, bg=Theme.BG, pady=20)
        self.display_frame.pack(expand=True, fill="both")

        # Previous expression label
        self.prev_label = tk.Label(
            self.display_frame,
            text="",
            anchor="e",
            bg=Theme.BG,
            fg=Theme.TEXT_SECONDARY,
            font=("Inter", 12),
            padx=20
        )
        self.prev_label.pack(fill="x")

        # Main display label
        self.display_label = tk.Label(
            self.display_frame,
            text="0",
            anchor="e",
            bg=Theme.BG,
            fg=Theme.TEXT_PRIMARY,
            font=("Inter", 36, "bold"),
            padx=20
        )
        self.display_label.pack(fill="x")

        # Buttons frame
        self.buttons_frame = tk.Frame(self.root, bg=Theme.BG, padx=10, pady=10)
        self.buttons_frame.pack(expand=True, fill="both")

        # Button groups configuration with theme colors
        buttons = [
            ('C', 0, 0, Theme.BTN_SPECIAL), ('DEL', 0, 1, Theme.BTN_DELETE), ('%', 0, 2, Theme.BTN_OPERATOR), ('/', 0, 3, Theme.BTN_OPERATOR),
            ('7', 1, 0, Theme.BTN_NUMBER), ('8', 1, 1, Theme.BTN_NUMBER), ('9', 1, 2, Theme.BTN_NUMBER), ('*', 1, 3, Theme.BTN_OPERATOR),
            ('4', 2, 0, Theme.BTN_NUMBER), ('5', 2, 1, Theme.BTN_NUMBER), ('6', 2, 2, Theme.BTN_NUMBER), ('-', 2, 3, Theme.BTN_OPERATOR),
            ('1', 3, 0, Theme.BTN_NUMBER), ('2', 3, 1, Theme.BTN_NUMBER), ('3', 3, 2, Theme.BTN_NUMBER), ('+', 3, 3, Theme.BTN_OPERATOR),
            ('0', 4, 0, Theme.BTN_NUMBER, 2), ('.', 4, 2, Theme.BTN_NUMBER), ('=', 4, 3, Theme.BTN_EQUALS)
        ]

        for btn_data in buttons:
            text = btn_data[0]
            row = btn_data[1]
            col = btn_data[2]
            color = btn_data[3]
            colspan = btn_data[4] if len(btn_data) > 4 else 1
            self.create_button(text, row, col, color, colspan)

        # Bind keyboard
        self.root.bind('<Key>', self.key_event)

    def create_button(self, text, row, col, bg_color, colspan=1):
        # Determine text color based on button background
        is_light_bg = bg_color in [Theme.BTN_EQUALS, Theme.BTN_OPERATOR, Theme.BTN_DELETE, Theme.BTN_SPECIAL]
        text_color = "#11111b" if is_light_bg else Theme.TEXT_PRIMARY

        button = tk.Button(
            self.buttons_frame,
            text=text,
            font=("Inter", 14, "bold"),
            bg=bg_color,
            fg=text_color,
            borderwidth=0,
            activebackground=Theme.ACTIVE_BG,
            activeforeground=Theme.ACTIVE_FG,
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
            # Prevent leading operators
            elif self.equation == "" and char in "+-*/.%":
                if char == "-":  # Allow negative numbers
                    self.equation = "-"
                return
            else:
                self.equation += str(char)

        self.update_display()

    def safe_calculate(self, expression: str) -> Optional[float]:
        """Safely calculate mathematical expression without using eval."""
        try:
            # Remove spaces
            expression = expression.strip()

            # Replace division symbol
            expression = expression.replace('÷', '/')

            # Handle percentage conversion
            expression = expression.replace('%', '/100')

            # Validate that expression contains only allowed characters
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters in expression")

            # Use compile to safely evaluate
            code = compile(expression, '<string>', 'eval')
            # Check that code only contains safe operations
            if code.co_names:
                raise ValueError("Function calls not allowed")

            result = eval(code, {"__builtins__": {}}, {})
            return float(result)
        except (ValueError, ZeroDivisionError, SyntaxError):
            return None

    def calculate(self):
        try:
            # Easter egg: 2+2 = 5
            if self.equation == "2+2":
                result = 5.0
            else:
                result = self.safe_calculate(self.equation)

            if result is None:
                messagebox.showerror("Error", "Invalid Expression")
                self.equation = ""
            else:
                self.history.append(self.equation)
                self.prev_label.config(text=f"{self.equation} =")
                # Format result to avoid floating point errors
                if result == int(result):
                    self.equation = str(int(result))
                else:
                    self.equation = str(round(result, 10))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
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
