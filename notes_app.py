import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
from datetime import datetime

# Файл для хранения данных
DATA_FILE = "notes_data.json"

class SimpleNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Мои Заметки")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

        self.notes = self.load_notes()
        self.current_note_index = None

        # Шрифты
        self.font_title = ("Arial", 12, "bold")
        self.font_text = ("Arial", 11)

        self.setup_ui()
        self.update_listbox()

    def setup_ui(self):
        # Панель слева (список)
        self.sidebar = tk.Frame(self.root, width=250, bg="#ffffff", bd=1, relief="solid")
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        tk.Label(self.sidebar, text="Список заметок", font=self.font_title, bg="#ffffff").pack(pady=10)

        self.listbox = tk.Listbox(self.sidebar, font=self.font_text, bd=0, highlightthickness=0)
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_note_select)

        btn_frame = tk.Frame(self.sidebar, bg="#ffffff")
        btn_frame.pack(fill="x", side="bottom", pady=5)

        tk.Button(btn_frame, text="+ Новая", command=self.add_note, bg="#4CAF50", fg="white", relief="flat").pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_note, bg="#f44336", fg="white", relief="flat").pack(side="left", expand=True, fill="x", padx=5)

        # Панель справа (редактор)
        self.editor = tk.Frame(self.root, bg="#f0f0f0")
        self.editor.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(self.editor, text="Заголовок:", bg="#f0f0f0", font=self.font_text).pack(anchor="w")
        self.title_entry = tk.Entry(self.editor, font=self.font_title, bd=1)
        self.title_entry.pack(fill="x", pady=5)
        self.title_entry.bind("<KeyRelease>", self.auto_save)

        tk.Label(self.editor, text="Текст заметки:", bg="#f0f0f0", font=self.font_text).pack(anchor="w")
        self.text_area = scrolledtext.ScrolledText(self.editor, font=self.font_text, bd=1, wrap="word")
        self.text_area.pack(fill="both", expand=True, pady=5)
        self.text_area.bind("<KeyRelease>", self.auto_save)

        self.status_label = tk.Label(self.editor, text="Готово", bg="#f0f0f0", fg="gray", font=("Arial", 9))
        self.status_label.pack(anchor="e")

    def load_notes(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_notes_to_file(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for note in self.notes:
            self.listbox.insert(tk.END, note.get("title") or "Без названия")

    def on_note_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.current_note_index = selection[0]
            note = self.notes[self.current_note_index]
            
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note["title"])
            
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", note["content"])
            self.status_label.config(text=f"Последнее изменение: {note.get('time', 'неизвестно')}")

    def add_note(self):
        new_note = {
            "title": "Новая заметка",
            "content": "",
            "time": datetime.now().strftime("%H:%M:%S")
        }
        self.notes.insert(0, new_note)
        self.save_notes_to_file()
        self.update_listbox()
        self.listbox.select_set(0)
        self.on_note_select(None)

    def delete_note(self):
        if self.current_note_index is not None:
            if messagebox.askyesno("Удаление", "Вы уверены, что хотите удалить эту заметку?"):
                del self.notes[self.current_note_index]
                self.current_note_index = None
                self.title_entry.delete(0, tk.END)
                self.text_area.delete("1.0", tk.END)
                self.save_notes_to_file()
                self.update_listbox()

    def auto_save(self, event=None):
        if self.current_note_index is not None:
            self.notes[self.current_note_index]["title"] = self.title_entry.get()
            self.notes[self.current_note_index]["content"] = self.text_area.get("1.0", tk.END).strip()
            self.notes[self.current_note_index]["time"] = datetime.now().strftime("%H:%M:%S")
            self.save_notes_to_file()
            
            # Обновляем заголовок в списке без перезагрузки всего списка для плавности
            self.listbox.delete(self.current_note_index)
            self.listbox.insert(self.current_note_index, self.notes[self.current_note_index]["title"])
            self.listbox.select_set(self.current_note_index)
            self.status_label.config(text="Сохранено")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleNotesApp(root)
    root.mainloop()
