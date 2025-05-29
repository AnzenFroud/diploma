import customtkinter as ctk
from tkinter import filedialog, colorchooser


class FileEntryGroup(ctk.CTkFrame):
    def __init__(self, parent, index, default_color="#ffffff"):
        super().__init__(parent)
        self.file_path_var = ctk.StringVar()
        self.inventory_column_var = ctk.StringVar()
        self.color = default_color

        self.configure(corner_radius=10, fg_color="#2a2a2a")

        title = ctk.CTkLabel(self, text=f"Файл {index}", font=ctk.CTkFont(size=14, weight="bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))

        file_label = ctk.CTkLabel(self, text="Путь к файлу:")
        file_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        file_entry = ctk.CTkEntry(self, textvariable=self.file_path_var, width=320)
        file_entry.grid(row=1, column=1, padx=5, pady=5)

        browse_button = ctk.CTkButton(self, text="Обзор", command=self.browse_file, width=80)
        browse_button.grid(row=1, column=2, padx=10, pady=5)

        inventory_label = ctk.CTkLabel(self, text="Столбец инв. номера:")
        inventory_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)

        inventory_entry = ctk.CTkEntry(self, textvariable=self.inventory_column_var, width=150)
        inventory_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Индикатор цвета
        self.color_box = ctk.CTkButton(self, text="", width=20, height=20, fg_color=self.color,
                                       command=self.change_color)
        self.color_box.grid(row=2, column=2, padx=10, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("CSV файлы", "*.csv"), ("Excel файлы", "*.xls *.xlsx"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

    def change_color(self):
        color_code = colorchooser.askcolor(title="Выберите цвет")[1]
        if color_code:
            self.color = color_code
            self.color_box.configure(fg_color=color_code)


class MarkStatementsForm(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Проверка инвентарных номеров")
        self.geometry("700x500")
        self.resizable(True, True)

        self.file_entries = []

        self.source_column_var = ctk.StringVar()

        source_frame = ctk.CTkFrame(self, corner_radius=10)
        source_frame.pack(fill="x", padx=15, pady=10)

        source_label = ctk.CTkLabel(source_frame, text="Столбец инв. номера в исходном файле:")
        source_label.pack(side="left", padx=10, pady=10)

        source_entry = ctk.CTkEntry(source_frame, textvariable=self.source_column_var, width=200)
        source_entry.pack(side="left", padx=5)

        button_frame = ctk.CTkFrame(self, corner_radius=10)
        button_frame.pack(fill="x", padx=15)

        check_button = ctk.CTkButton(button_frame, text="Проверить", command=self.check_statements)
        check_button.pack(side="left", padx=5, pady=10)

        add_file_button = ctk.CTkButton(button_frame, text="Добавить файл", command=self.add_file_entry)
        add_file_button.pack(side="left", padx=5, pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.scrollable_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.add_file_entry()

    def add_file_entry(self):
        index = len(self.file_entries) + 1
        group = FileEntryGroup(self.scrollable_frame, index)
        group.pack(fill="x", padx=10, pady=10)
        self.file_entries.append(group)

    def check_statements(self):
        for idx, group in enumerate(self.file_entries, start=1):
            print(f"Файл {idx}: {group.file_path_var.get()}")
            print(f"  Столбец инв. номера: {group.inventory_column_var.get()}")
            print(f"  Цвет: {group.color}")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.withdraw()
    MarkStatementsForm(root)
    root.mainloop()
