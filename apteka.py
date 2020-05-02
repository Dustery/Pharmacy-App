import tkinter as tk
from tkinter import ttk
import sqlite3
import time
import webbrowser
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

        # Добавление иконок
        self.add_img = ImageTk.PhotoImage(file='icon\medical-history.png')
        self.edit_img = ImageTk.PhotoImage(file='icon\pencil.png')
        self.delete_img = ImageTk.PhotoImage(file='icon\delete.png')
        self.search_img = ImageTk.PhotoImage(file='icon\search.png')
        self.update_img = ImageTk.PhotoImage(file='icon\\update.png')
        self.info_img = ImageTk.PhotoImage(file='icon\info.png')

        # КНОПКИ ТУЛБАРА
        # Кнопка вызова окна добавления препарата
        btn_open_dialog = tk.Button(toolbar,
                                    text = 'Добавить позицию',
                                    command = self.open_dialog,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.add_img,
                                    padx = 5
                                    )
        btn_open_dialog.pack(side = tk.LEFT)

        # Кнопка вызова окна редактирования
        btn_edit_dialog = tk.Button(toolbar,
                                    text = 'Редактировать',
                                    command = self.open_update_dialog,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.edit_img
                                    )
        btn_edit_dialog.pack(side = tk.LEFT)

        # Кнопка удаления записей
        btn_delete = tk.Button(toolbar,
                                    text = 'Удалить',
                                    command = self.delete_records,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.delete_img,
                                    padx = 5
                                    )
        btn_delete.pack(side = tk.LEFT)

        # Кнопка поиска записей
        btn_search = tk.Button(toolbar,
                                    text = 'Поиск',
                                    command = self.open_search_dialog,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.search_img,
                                    padx = 10
                                    )
        btn_search.pack(side = tk.LEFT)

        # Кнопка обновление таблицы и записей
        btn_update = tk.Button(toolbar,
                                    text = 'Обновить',
                                    command = self.view_records,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.update_img,
                                    padx = 7
                                    )
        btn_update.pack(side = tk.LEFT)

        # Кнопка информация
        btn_update = tk.Button(toolbar,
                                    text = 'О программе',
                                    command = self.view_info,
                                    bg = '#d7d8e0',
                                    bd = 0,
                                    compound = tk.TOP,
                                    image = self.info_img,
                                    padx = 13
                                    )
        btn_update.pack(side = tk.LEFT)

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

        # Дата и время
        def get_time(): 
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            clock.config(text=date)
            clock.after(200,get_time)
        
        clock = tk.Label(self, font=('bold', 13))
        clock.pack(side = tk.BOTTOM)
        get_time()

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

    def search_records(self, name):
        name = ('%' + name + '%', )
        self.db.c.execute('''SELECT * FROM medkit WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()
    
    def open_update_dialog(self):
        Edit()

    def open_search_dialog(self):
        Search()

    def view_info(self):
        Info()


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

class Edit(Child):
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

# Поиск данных в таблице базы SQLite
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x = 50, y = 20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x = 105, y = 20, width = 150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x = 182, y = 50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x = 103, y = 50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


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

# Класс информация о программе
class Info(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.info_window()
        #self.view = app


    def info_window(self):
        self.title('О программе')
        self.geometry('370x200+400+300')
        self.resizable(False, False)
        
        self.facebook_img = ImageTk.PhotoImage(file='icon\\facebook.png')
        self.instagram_img = ImageTk.PhotoImage(file='icon\\instagram.png')

        def callback(url):
            webbrowser.open_new(url)

        about_name = tk.Label(self, text = 'АПТЕЧКА',
                            fg = 'black',
                            bd = 0,
                            font=('bold', 16),
                        )
        about_name.place(x = 140, y = 10)

        about = tk.Label(self, text = 'Приложение для ведения учета\nмед.препаратов',
                            fg = 'black',
                            bd = 0,
                            font=('bold', 12)
                        )
        about.place(x = 70, y = 35)

        btn_facebook = tk.Label(self, image = self.facebook_img, cursor='hand2')
        btn_facebook.place(x = 130, y = 90)
        btn_facebook.bind("<Button-1>", lambda e: callback("https://www.facebook.com/kostynskyi95"))
    
        btn_instagram = tk.Label(self, image = self.instagram_img, cursor='hand2')
        btn_instagram.place(x = 200, y = 90)
        btn_instagram.bind("<Button-1>", lambda e: callback("https://www.instagram.com/olek_kost"))

        about_author = tk.Label(self, text = 'Автор: Oleksandr Kostynskyi',
                            fg = 'black',
                            cursor = 'hand2',
                            bd = 0,
                            font=('Consolas', 11)
                        )
        about_author.place(x = 20, y = 150)

        about_version = tk.Label(self, text = 'Версия: 1.2',
                            fg = 'black',
                            bd = 0,
                            font=('Consolas', 11)
                        )
        about_version.place(x = 20, y = 170)
       
# Start App
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Аптечка')
    root.iconphoto(True, ImageTk.PhotoImage(file=".//icon//healthcare.png"))
    root.geometry('650x450+300+150')
    root.resizable(False, False)
    root.mainloop()