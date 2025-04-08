# import tkinter as tk

# root = tk.Tk() # Вызов класса
# root.title("Tkinter Test") # название окна
# root.geometry("500x500+200+200") #размер + позицонирование относительно верхнего левого угла
# label = tk.Label(root, text="Hello, Tkinter!",
#                  bg = "blue",
#                  fg = "white",
#                  font = ("Aria",20,"bold")
#                  ) # виджет - поле текста, где распологаем, значение
# label1= tk.Label(root, text="Hello, Tkinter!",
#                  bg = "blue",
#                  fg = "white",
#                  font = ("Aria",20,"bold")
#                  ) # виджет - поле текста, где распологаем, значение
# label2= tk.Label(root, text="Hello, Tkinter!",
#                  bg = "blue",
#                  fg = "white",
#                  font = ("Aria",20,"bold")
#                  ) # виджет - поле текста, где распологаем, значение
# label.grid(row=0,column=0) #менджер геометрии виджета -  упаковщик/сетка/размещение по координатам
# label1.grid(row=1,column=1,columnspan=1)
# # label2.grid(row=2,column=0,columnspan=) #менджер геометрии виджета -  упаковщик/сетка/размещение по координатам
# root.mainloop() #запуск главного цикла для отображения окна
# #которое переходит в режим ожидания
import tkinter as tk
from pandastable import Table

root = tk.Tk()

frame = tk.Frame(root)
frame.pack()

pt = Table(frame)
pt.show()

root.mainloop()
