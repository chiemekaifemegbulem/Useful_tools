import tkinter as tk
from tkinter import messagebox
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Calculator")
        self.geometry("400x700")
        self.resizable(False, False)
        self.configure(bg="#121212")
        
        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        self.entry = tk.Entry(self, font=("Arial", 32), bd=5, relief=tk.FLAT, justify='right', bg="#1E1E1E", fg="white", insertbackground="white")
        self.entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, pady=10, padx=10, sticky="nsew")
        
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('.', 4, 2), ('+', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('^', 5, 2), ('√', 5, 3),
            ('%', 6, 0), ('DEL', 6, 1), ('EXP', 6, 2), ('1/x', 6, 3),
            ('±', 7, 0), ('π', 7, 1), ('e', 7, 2), ('=', 7, 3)
        ]
        
        for text, row, col in buttons:
            btn = tk.Button(self, text=text, font=("Arial", 22, "bold"), bg="#2A2A2A", fg="white", bd=2, relief=tk.RAISED,
                            activebackground="#444444", activeforeground="white", highlightthickness=0, cursor="hand2",
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, ipadx=30, ipady=20, padx=5, pady=5, sticky="nsew")
        
        for i in range(10):
            self.rowconfigure(i, weight=1)
        for i in range(4):
            self.columnconfigure(i, weight=1)
    
    def on_button_click(self, char):
        try:
            if char == "C":
                self.expression = ""
            elif char == "DEL":
                self.expression = self.expression[:-1]
            elif char == "=":
                self.expression = str(eval(self.expression.replace("^", "**")))
            elif char == "√":
                self.expression = str(math.sqrt(eval(self.expression)))
            elif char == "1/x":
                self.expression = str(1 / eval(self.expression))
            elif char == "EXP":
                self.expression += "*10**"
            elif char == "π":
                self.expression += str(math.pi)
            elif char == "e":
                self.expression += str(math.e)
            elif char == "±":
                if self.expression:
                    self.expression = str(eval(self.expression) * -1)
            elif char == "%":
                if self.expression:
                    self.expression = str(eval(self.expression) / 100)
            else:
                self.expression += char
            self.update_entry()
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Cannot divide by zero")
            self.expression = ""
            self.update_entry()
        except SyntaxError:
            messagebox.showerror("Syntax Error", "Invalid input")
            self.expression = ""
            self.update_entry()
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.expression = ""
            self.update_entry()
    
    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
