import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
 
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill = tk.X)
        
        # Подпись, версия
        some_text = tk.Label(toolbar,
                            text = '"Аптечка"\nПриложение для ведения учета мед.препаратов\nАвтор: Oleksandr Kostynskyi\nВерсия: 1.0',
                            fg = 'grey',
                            bg = '#d7d8e0',
                            bd = 0
                            )
        some_text.pack(side = tk.RIGHT)

        # Добавление иконок
        self.add_img = ImageTk.PhotoImage(file='icon\medical-history.png')
        self.update_img = ImageTk.PhotoImage(file='icon\pencil.png')
        self.delete_img = ImageTk.PhotoImage(file='icon\delete.png')

        # Кнопка вызова окна добавления препарата
        btn_open_dialog = tk.Button(toolbar,
                                    text = 'Добавить позицию',
                                    command = self.open_dialog,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.add_img
                                    )
        btn_open_dialog.pack(side = tk.LEFT)

        #Кнопка вызова окна редактирования
        btn_edit_dialog = tk.Button(toolbar,
                                    text = 'Редактировать',
                                    command = self.open_update_dialog,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.update_img
                                    )
        btn_edit_dialog.pack(side = tk.LEFT)

        #Кнопка удаления записей
        btn_delete = tk.Button(toolbar,
                                    text = 'Удалить',
                                    command = self.delete_records,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.delete_img
                                    )
        btn_delete.pack(side = tk.LEFT)

        # Добавление таблицы в окно программы
        self.tree = ttk.Treeview(self, columns = ('ID', 'name', 'time', 'total'), height = 15, show = 'headings')
        self.tree.column('ID', width = 30, anchor = tk.CENTER)
        self.tree.column('name', width = 355, anchor = tk.CENTER)
        self.tree.column('time', width = 160, anchor = tk.CENTER)
        self.tree.column('total', width = 100, anchor = tk.CENTER)

        self.tree.heading('ID', text = '№')
        self.tree.heading('name', text = 'Название лекарства')
        self.tree.heading('time', text = 'Срок годности')
        self.tree.heading('total', text = 'Количество')
        self.tree.pack()

    def records(self, name, time, total):
        self.db.insert_data(name, time, total)
        self.view_records()

    def update_records(self, name, time, total):
        self.db.c.execute(
            '''UPDATE medkit SET name=?, time=?, total=? WHERE ID=?''',
            (name, time, total, self.tree.set(self.tree.selection()[0], '#1'))
        )
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute(
            '''SELECT * FROM medkit'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute(
                '''DELETE FROM medkit WHERE id=?''', (self.tree.set(selection_item, '#1'),)
            )
        self.db.conn.commit()
        self.view_records()

    def open_dialog(self):
        Child()
    
    def open_update_dialog(self):
        Update()

# Класс дочерних окон
class Child (tk.Toplevel):      
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Дочернее окно добавления лекарства
    def init_child(self):
        self.title('Добавить препарат')
        self.geometry('400x300+300+150')
        self.resizable(False, False)

        self.label_name = tk.Label(self, text = 'Название лекарства')
        self.label_name.place(x = 50, y = 50)
        self.label_time = tk.Label(self, text = 'Срок годности')
        self.label_time.place(x = 50, y = 110)
        self.label_total = tk.Label(self, text = 'Количество')
        self.label_total.place(x = 50, y = 170)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x = 200, y = 50)
        self.entry_time = ttk.Entry(self)
        self.entry_time.place(x = 200, y = 110)
        self.entry_total = ttk.Entry(self)
        self.entry_total.place(x = 200, y = 170)

        self.btn_close = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        self.btn_close.place(x = 220, y = 250)
        self.btn_add = ttk.Button(self, text = 'Добавить')
        self.btn_add.place(x = 115, y = 250)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(), self.entry_time.get(), self.entry_total.get()))

        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    
    def init_edit(self):
        self.title('Редактировать')
        btn_edit = ttk.Button(self, text = 'Редактировать')
        btn_edit.place(x = 210, y = 250)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_name.get(), self.entry_time.get(), self.entry_total.get()))
        self.btn_close.destroy()


# Класс для работы с базой данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('medkit.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS medkit (id integer primary key, name text, time text, total real)'''
        )
        self.conn.commit()
    
    def insert_data(self, name, time, total):
        self.c.execute(
            '''INSERT INTO medkit(name, time, total) VALUES (?, ?, ?)''', (name, time, total)
        )
        self.conn.commit()

       
# Start App
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Аптечка')
    root.iconphoto(True, ImageTk.PhotoImage(file="./icon/healthcare.png"))
    root.geometry('650x450+300+150')
    root.resizable(False, False)
    root.mainloop()