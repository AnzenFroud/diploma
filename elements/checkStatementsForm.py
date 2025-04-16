import tkinter as tk
from tkinter import filedialog

class FileEntryGroup(tk.LabelFrame):
    def __init__(self, parent, index):
        super().__init__(
            parent,
            text=f"Файл {index}",
            relief='groove',
            borderwidth=2,
            padx=10,
            pady=10
        )
        
        self.file_path_var = tk.StringVar()
        self.name_column_var = tk.StringVar()
        self.inventory_column_var = tk.StringVar()

        # Поле для ввода пути к файлу
        file_label = tk.Label(self, text="Путь к файлу:")
        file_label.grid(row=0, column=0, sticky='e', padx=5, pady=2)

        file_entry = tk.Entry(self, textvariable=self.file_path_var, width=40)
        file_entry.grid(row=0, column=1, padx=5, pady=2)

        browse_button = tk.Button(self, text="Обзор", command=self.browse_file)
        browse_button.grid(row=0, column=2, padx=5, pady=2)

        # Поле для ввода названия столбца с наименованием
        name_label = tk.Label(self, text="Столбец с наименованием:")
        name_label.grid(row=1, column=0, sticky='e', padx=5, pady=2)

        name_entry = tk.Entry(self, textvariable=self.name_column_var, width=30)
        name_entry.grid(row=1, column=1, padx=5, pady=2, columnspan=2, sticky='w')

        # Поле для ввода названия столбца с инвентарным номером
        inventory_label = tk.Label(self, text="Столбец с инвентарным номером:")
        inventory_label.grid(row=2, column=0, sticky='e', padx=5, pady=2)

        inventory_entry = tk.Entry(self, textvariable=self.inventory_column_var, width=30)
        inventory_entry.grid(row=2, column=1, padx=5, pady=2, columnspan=2, sticky='w')

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("CSV файлы", "*.csv"), ("Excel файлы", "*.xls *.xlsx"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

class CheckStatementsForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Проверка наименований")
        self.geometry("600x400")
        self.resizable(True, True)

        self.file_entries = []

        # Создание холста и полосы прокрутки
        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(container, borderwidth=0)
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Создание фрейма внутри холста
        self.entries_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.entries_frame, anchor="nw")

        # Обновление области прокрутки при изменении размера содержимого
        self.entries_frame.bind("<Configure>", self.on_frame_configure)

        # Привязка событий прокрутки мыши
        self.bind_mousewheel_events()

        # Кнопка для добавления новой группы ввода
        add_button = tk.Button(self, text="Добавить файл", command=self.add_file_entry)
        add_button.pack(pady=5)

        # Кнопка для запуска проверки
        check_button = tk.Button(self, text="Проверить", command=self.check_statements)
        check_button.pack(pady=5)

        # Добавляем первую группу ввода по умолчанию
        self.add_file_entry()

    def bind_mousewheel_events(self):
        # Windows и MacOS
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        # Linux
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)

    def on_mousewheel(self, event):
        # Windows и MacOS
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_file_entry(self):
        index = len(self.file_entries) + 1
        group = FileEntryGroup(self.entries_frame, index)
        group.pack(fill='x', pady=5)
        self.file_entries.append(group)

    def check_statements(self):
        for idx, group in enumerate(self.file_entries, start=1):
            file_path = group.file_path_var.get()
            name_column = group.name_column_var.get()
            inventory_column = group.inventory_column_var.get()
            print(f"Группа {idx}:")
            print(f"  Файл: {file_path}")
            print(f"  Столбец с наименованием: {name_column}")
            print(f"  Столбец с инвентарным номером: {inventory_column}")
            # Здесь можно добавить логику обработки каждого файла

# Пример использования
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно
    CheckStatementsForm(root)
    root.mainloop()
