import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("dark")  # Темная тема
ctk.set_default_color_theme("blue")  # Можно поменять на "green", "dark-blue" и др.

class FileEntryGroup(ctk.CTkFrame):
    def __init__(self, parent, index):
        super().__init__(parent)
        
        self.file_path_var = ctk.StringVar()
        self.name_column_var = ctk.StringVar()
        self.inventory_column_var = ctk.StringVar()

        # Заголовок
        title = ctk.CTkLabel(self, text=f"Файл {index}", font=ctk.CTkFont(size=16, weight="bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        # Путь к файлу
        ctk.CTkLabel(self, text="Путь к файлу:").grid(row=1, column=0, sticky="e", padx=5, pady=4)
        ctk.CTkEntry(self, textvariable=self.file_path_var, width=300).grid(row=1, column=1, padx=5, pady=4)
        ctk.CTkButton(self, text="Обзор", width=80, command=self.browse_file).grid(row=1, column=2, padx=5, pady=4)

        # Столбец с наименованием
        ctk.CTkLabel(self, text="Столбец с наименованием:").grid(row=2, column=0, sticky="e", padx=5, pady=4)
        ctk.CTkEntry(self, textvariable=self.name_column_var, width=250).grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=4)

        # Столбец с инвентарным номером
        ctk.CTkLabel(self, text="Столбец с инвентарным номером:").grid(row=3, column=0, sticky="e", padx=5, pady=4)
        ctk.CTkEntry(self, textvariable=self.inventory_column_var, width=250).grid(row=3, column=1, columnspan=2, sticky="w", padx=5, pady=4)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("CSV файлы", "*.csv"), ("Excel файлы", "*.xls *.xlsx"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

class CheckStatementsForm(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Проверка наименований")
        self.geometry("640x500")
        self.resizable(True, True)

        self.file_entries = []

        # Основной контейнер с прокруткой
        container = ctk.CTkScrollableFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.entries_frame = container

        # Кнопки
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(5, 10))

        ctk.CTkButton(button_frame, text="Добавить файл", command=self.add_file_entry).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Проверить", command=self.check_statements).pack(side="left", padx=10)

        # Добавляем первую группу по умолчанию
        self.add_file_entry()

    def add_file_entry(self):
        index = len(self.file_entries) + 1
        group = FileEntryGroup(self.entries_frame, index)
        group.pack(fill="x", pady=10, padx=10)
        self.file_entries.append(group)

    def check_statements(self):
        for idx, group in enumerate(self.file_entries, start=1):
            print(f"Группа {idx}:")
            print(f"  Файл: {group.file_path_var.get()}")
            print(f"  Столбец с наименованием: {group.name_column_var.get()}")
            print(f"  Столбец с инвентарным номером: {group.inventory_column_var.get()}")

# Запуск
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()  # Скрываем основное окно
    CheckStatementsForm(root)
    root.mainloop()
