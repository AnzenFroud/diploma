import tkinter as tk
from pandastable import Table, TableModel
from pandastable.core import ToolBar
import pandas as pd

from checkStatementsForm import CheckStatementsForm
def open_check_statements():
    CheckStatementsForm(root)

from markStatementsForm import MarkStatementsForm
def open_mark_statements():
    MarkStatementsForm(root)   

class HorizontalToolBar(ToolBar):
    def createButtons(self):
        for button in self.bnames:
            self.bimages[button] = self.master.parent.app.getImage(button)
            b = tk.Button(self, image=self.bimages[button], command=self.bcommands[button])
            b.image = self.bimages[button]
            b.pack(side='top', padx=2, pady=2)
            self.buttons[button] = b

def toggle_toolbar():
    if toolbar_frame.winfo_ismapped():
        toolbar_frame.pack_forget()
        toggle_btn.config(text="Показать панель инструментов")
    else:
        toolbar_frame.pack(side='right', fill='y')
        toggle_btn.config(text="Скрыть панель инструментов")

def additional_action():
    print("Дополнительное действие выполнено")

root = tk.Tk()
root.title("Реестр оборудования")
root.geometry("800x600+200+200")

# Основной фрейм
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Фрейм для кнопок управления
control_frame = tk.Frame(main_frame)
control_frame.pack(side='top', fill='x')

# Кнопка для отображения/скрытия панели инструментов
toggle_btn = tk.Button(control_frame, text="Показать панель инструментов", command=toggle_toolbar)
toggle_btn.pack(side='left', padx=5, pady=5)

# Дополнительнst кнопки
check_statments = tk.Button(control_frame, text="Проверить наименования",command=open_check_statements)
check_statments.pack(side='left', padx=5, pady=5)
mark_statments = tk.Button(control_frame, text="Отметить оборудование", command=open_mark_statements)
mark_statments.pack(side='left', padx=5, pady=5)
make_sticker = tk.Button(control_frame, text="Сделать этикетку", command=open_mark_statements)
make_sticker.pack(side='left', padx=5, pady=5)
# Фрейм для панели инструментов
toolbar_frame = tk.Frame(main_frame)

# Фрейм для таблицы
table_frame = tk.Frame(main_frame)
table_frame.pack(fill='both', expand=True, side='left')

# Получаем пример данных как DataFrame
data_dict = TableModel.getSampleData()
df = pd.DataFrame(data_dict)

# Создаём модель на основе DataFrame
model = TableModel(dataframe=df)

# Инициализация таблицы без встроенной панели инструментов
pt = Table(table_frame, model=model, showtoolbar=False, showstatusbar=True)
pt.show()

# Создание панели инструментов
toolbar = HorizontalToolBar(toolbar_frame, pt)
toolbar.pack(side='top', anchor='w')

root.mainloop()





