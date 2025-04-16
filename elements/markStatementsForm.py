import tkinter as tk
from tkinter import filedialog, colorchooser

class FileEntryGroup(tk.LabelFrame):
    def __init__(self, parent, index, highlight_color):
        super().__init__(parent, text=f"Файл {index}", relief="groove", borderwidth=2, padx=10, pady=10)
        self.file_path_var = tk.StringVar()
        self.inventory_column_var = tk.StringVar()

        # Поле для ввода пути к файлу
        file_label = tk.Label(self, text="Путь к файлу:")
        file_label.grid(row=0, column=0, sticky="e", padx=5, pady=2)

        file_entry = tk.Entry(self, textvariable=self.file_path_var, width=40)
        file_entry.grid(row=0, column=1, padx=5, pady=2)

        browse_button = tk.Button(self, text="Обзор", command=self.browse_file)
        browse_button.grid(row=0, column=2, padx=5, pady=2)

        # Поле для ввода названия столбца с инвентарным номером
        inventory_label = tk.Label(self, text="Столбец с инвентарным номером:")
        inventory_label.grid(row=1, column=0, sticky="e", padx=5, pady=2)

        inventory_entry = tk.Entry(self, textvariable=self.inventory_column_var, width=30)
        inventory_entry.grid(row=1, column=1, padx=5, pady=2, columnspan=2, sticky="w")

        # Установка цвета фона
        self.configure(bg=highlight_color)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("CSV файлы", "*.csv"), ("Excel файлы", "*.xls *.xlsx"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

class MarkStatementsForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Проверка инвентарных номеров")
        self.geometry("600x500")
        self.resizable(True, True)

        self.file_entries = []
        self.highlight_color = "#ffffff"  # Начальный цвет подсветки

        # Поле для указания названия столбца с инвентарным номером из исходного файла
        source_frame = tk.Frame(self)
        source_frame.pack(fill="x", padx=10, pady=10)

        source_label = tk.Label(source_frame, text="Столбец с инвентарным номером в исходном файле:")
        source_label.pack(side="left")

        self.source_column_var = tk.StringVar()
        source_entry = tk.Entry(source_frame, textvariable=self.source_column_var, width=30)
        source_entry.pack(side="left", padx=5, pady=2)

        # Кнопка для запуска проверки
        check_button = tk.Button(self, text="Проверить", command=self.check_statements)
        check_button.pack(pady=5)

        # Кнопка для выбора цвета подсветки
        color_button = tk.Button(self, text="Выбрать цвет подсветки", command=self.choose_highlight_color)
        color_button.pack(pady=5)

        # Создание холста и полосы прокрутки
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container)
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
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # Добавляем первую группу ввода по умолчанию
        self.add_file_entry()

        # Кнопка "Добавить файл" внизу
        add_file_button = tk.Button(self, text="Добавить файл", command=self.add_file_entry)
        add_file_button.pack(side="bottom", pady=10)

        # Обработка закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def choose_highlight_color(self):
        color_code = colorchooser.askcolor(title="Выберите цвет подсветки")[1]
        if color_code:
            self.highlight_color = color_code
            # Обновляем цвет фона у всех существующих групп
            for group in self.file_entries:
                group.configure(bg=color_code)

    def add_file_entry(self):
        index = len(self.file_entries) + 1
        group = FileEntryGroup(self.entries_frame, index, self.highlight_color)
        group.pack(fill="x", padx=5, pady=5)
        self.file_entries.append(group)

    def check_statements(self):
        # Логика проверки инвентарных номеров
        pass

    def on_frame_configure(self, event):
        if self.canvas.winfo_exists():
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_close(self):
        # Отменяем все привязки событий, чтобы избежать ошибок после закрытия окна
        self.canvas.unbind_all("<MouseWheel>")
        self.destroy()
