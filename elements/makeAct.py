from docx import Document
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import datetime
import os
import platform
import subprocess

def generate_act(table):
    # Получаем индекс выделенной строки
    row_index = table.getSelectedRow()
    if row_index is None:
        messagebox.showwarning("Выбор строки", "Пожалуйста, выделите строку в таблице.")
        return

    # Получаем данные строки как словарь
    row_data = table.model.getRecordAtRow(row_index)

    # Создание окна для выбора типа акта
    act_window = tk.Toplevel()
    act_window.title("Создание акта")
    act_window.geometry("400x300")

    act_type_var = tk.StringVar()
    act_types = ['Акт приема-передачи', 'Акт осмотра', 'Акт списания']
    act_type_var.set(act_types[0])  # По умолчанию первый тип акта

    # Выпадающий список для типа акта
    act_type_label = tk.Label(act_window, text="Выберите тип акта:")
    act_type_label.pack(pady=5)
    act_type_menu = tk.OptionMenu(act_window, act_type_var, *act_types)
    act_type_menu.pack(pady=5)

    # Метка и поле для ввода пути сохранения
    path_label = tk.Label(act_window, text="Путь для сохранения:")
    path_label.pack(pady=5)
    path_entry = tk.Entry(act_window, width=40)
    path_entry.pack(pady=5)

    # Кнопка для выбора пути через диалог
    def select_path():
        path = filedialog.askdirectory(initialdir=os.getcwd(), title="Выберите папку для сохранения")
        if path:
            path_entry.delete(0, tk.END)  # Очищаем текущее значение в поле
            path_entry.insert(0, path)    # Вставляем выбранный путь

    select_button = tk.Button(act_window, text="Выбрать папку", command=select_path)
    select_button.pack(pady=5)

    # Кнопка для создания акта
    def create_act():
        act_type = act_type_var.get()
        save_path = path_entry.get()

        if not save_path:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите путь для сохранения.")
            return

        # Получаем данные для акта
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        doc = Document()

        # Заголовок акта
        doc.add_heading(f"{act_type}", 0)
        doc.add_paragraph(f"Дата: {today}")
        
        doc.add_paragraph("Данные о строке:")
        for col, value in row_data.items():
            doc.add_paragraph(f"{col}: {value}")

        # Имя файла с сегодняшней датой
        filename = f"{act_type.replace(' ', '_').lower()}_{today}.docx"
        filepath = os.path.join(save_path, filename)
        doc.save(filepath)

        # Попытка открыть файл
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.call(["open", filepath])
            elif platform.system() == "Windows":
                os.startfile(filepath)
            elif platform.system() == "Linux":
                subprocess.call(["xdg-open", filepath])
        except Exception as e:
            messagebox.showinfo("Готово", f"Документ создан, но не удалось открыть файл:\n{filepath}\n\n{e}")
            act_window.destroy()
            return

        messagebox.showinfo("Готово", f"Документ успешно создан:\n{filepath}")
        act_window.destroy()

    # Кнопка для создания акта
    generate_btn = tk.Button(act_window, text="Создать акт", command=create_act)
    generate_btn.pack(pady=20)
