import tkinter as tk
import customtkinter as ctk
from pandastable import Table, TableModel
import pandas as pd
from PIL import Image

from checkStatementsForm import CheckStatementsForm
from markStatementsForm import MarkStatementsForm
from maketag import generate_sticker
from makeAct import generate_act

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Загрузка иконок размером 24x24
def load_icon(name):
    path = f"../images/{name}.jpeg"
    img = Image.open(path).resize((24,24), Image.Resampling.LANCZOS)
    return ctk.CTkImage(img)

icon_search = load_icon("search")
icon_colorfill = load_icon("colorfill")
icon_document = load_icon("document")
icon_instruments = load_icon("instruments")
icon_tag = load_icon("tag")

def open_check_statements():
    CheckStatementsForm(root)

def open_mark_statements():
    MarkStatementsForm(root)

def make_sticker():
    generate_sticker(pt)

def make_act():
    generate_act(pt)

def toggle_toolbar():
    if toolbar_frame.winfo_ismapped():
        toolbar_frame.pack_forget()
        toggle_btn.configure(text="Показать панель инструментов")
    else:
        toolbar_frame.pack(side='right', fill='y')
        toggle_btn.configure(text="Скрыть панель инструментов")

# Главное окно
root = tk.Tk()
root.title("Реестр оборудования")
root.geometry("1000x600")

# ---------- Верхняя панель управления (в две строки) ----------
top_control_container = tk.Frame(root)
top_control_container.pack(fill='x')

# Первая строка кнопок
top_control_frame1 = ctk.CTkFrame(top_control_container)
top_control_frame1.pack(fill='x', padx=10, pady=(10, 5))

# Вторая строка с поиском
top_control_frame2 = ctk.CTkFrame(top_control_container)
top_control_frame2.pack(fill='x', padx=10, pady=(0, 10))

toggle_btn = ctk.CTkButton(top_control_frame1, 
                           text="Показать панель инструментов", 
                           command=toggle_toolbar,
                           image=icon_instruments,
                           compound="left")
toggle_btn.pack(side='left', padx=5)

check_btn = ctk.CTkButton(top_control_frame1, 
                          text="Проверить наименования", 
                          command=open_check_statements,
                          image=icon_search,
                          compound="left")
check_btn.pack(side='left', padx=5)

mark_btn = ctk.CTkButton(top_control_frame1, 
                         text="Отметить оборудование", 
                         command=open_mark_statements,
                         image=icon_colorfill,
                         compound="left")
mark_btn.pack(side='left', padx=5)

sticker_btn = ctk.CTkButton(top_control_frame1, 
                            text="Сделать этикетку", 
                            command=make_sticker,
                            image=icon_tag,
                            compound="left")
sticker_btn.pack(side='left', padx=5)

act_btn = ctk.CTkButton(top_control_frame1, 
                        text="Создать акт", 
                        command=make_act,
                        image=icon_document,
                        compound="left")
act_btn.pack(side='left', padx=5)

# Поисковое поле
def filter_table(event):
    search_text = search_var.get().lower()
    filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_text).any(), axis=1)]
    pt.updateModel(TableModel(filtered_df))
    pt.redraw()

search_label = ctk.CTkLabel(top_control_frame2, text="Поиск:")
search_label.pack(side='left', padx=(0,5))
search_var = tk.StringVar()
search_entry = ctk.CTkEntry(top_control_frame2, textvariable=search_var, width=300)
search_entry.pack(side='left')
search_entry.bind("<KeyRelease>", filter_table)

# ---------- Основная часть ----------
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Фрейм таблицы
table_frame = tk.Frame(main_frame)
table_frame.pack(side='left', fill='both', expand=True)

# Пример данных
data_dict = TableModel.getSampleData()
df = pd.DataFrame(data_dict)
model = TableModel(dataframe=df)

# Таблица
pt = Table(table_frame, model=model, showtoolbar=False, showstatusbar=True)

pt.cellbackgr = '#222222'           # фон ячеек
pt.cellfg = 'white'                 # цвет текста в ячейках
pt.grid_color = 'white'            # цвет сетки
pt.textcolor = 'white'             # дублируется, используется в заголовках
pt.rowselectedcolor = "#227AC2"    # цвет выделения строк
pt.colselectedcolor = "#227AC2"    # цвет выделения столбца

pt.colheadercolor = '#222222'      # фон заголовков столбцов
pt.colheaderfg = 'white'           # текст заголовков столбцов
pt.rowheadercolor = '#222222'      # фон заголовков строк
pt.rowheaderfg = 'white'           # текст заголовков строк

pt.font = 'Arial 10'               # шрифт в таблице
pt.boxoutlinecolor = 'white'       # цвет границ ячеек

pt.show()

# Фрейм панели инструментов
toolbar_frame = tk.Frame(main_frame)
toolbar_frame.pack(side='right', fill='y')  # Изначально видно

# Встроенный тулбар
from pandastable.core import ToolBar
class HorizontalToolBar(ToolBar):
    def createButtons(self):
        for button in self.bnames:
            self.bimages[button] = self.master.parent.app.getImage(button)
            b = tk.Button(self, image=self.bimages[button], command=self.bcommands[button])
            b.image = self.bimages[button]
            b.pack(side='top', padx=2, pady=2)
            self.buttons[button] = b

toolbar = HorizontalToolBar(toolbar_frame, pt)
toolbar.pack(side='top', anchor='w')

# Выбор строки по клику
pt.bind("<ButtonRelease-1>", lambda event: pt.setSelectedRow(pt.get_row_clicked(event)))

root.mainloop()