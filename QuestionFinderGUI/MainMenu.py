import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import threading


class MainMenu(tk.Menu):

    def __init__(self, controller, master=None, callback = None, cnf={}, **kw):

        # Settle it out
        super().__init__(master, cnf, **kw)
        self.operationMenu = tk.Menu(self, tearoff=0)
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.callback = callback

        self.my_controller = controller

        # 初始化Menu
        self.initFileMenu()
        self.init_Operation_Menu()

    def initFileMenu(self):
        self.add_cascade(labe='文件', menu=self.fileMenu)

        # Create the top line menu with following functions
        # file_menu_label = ['新建', '打开', '保存']
        # file_menu_command = [self.create_new, self.open_file, self.save_file]

        # Create the top line menu with following functions
        file_menu_label = ['新建']
        file_menu_command = [self.create_new]
        for i in range(len(file_menu_label)):
            self.fileMenu.add_command(label=file_menu_label[i], command=file_menu_command[i])
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='关闭', command=self.quit)
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        self.save_file()
        self.master.destroy()

    def create_new(self):
        self.save_file()

        filename = askdirectory()
        self.master.update()

        self.my_controller.set_question_from_pictures(filename)

        root = tk.Toplevel()
        root.title("QFinderEditor")
        root.geometry("1000x800")

        widget = tk.Text(root, width=140, height=50,
                         background='Gray', wrap='word')

        widget.pack()

        widget.insert(tk.CURRENT, "-----------------------------请让每个问题之间空一行------------------------\n")
        widget.insert(tk.CURRENT, "-----------------------------每个问题内部不允许空行------------------------\n")

        suffix = 1
        while os.path.exists('data/output%d.txt' % suffix):
            file = open('data/output%d.txt' % suffix)
            suffix += 1
            for line in file.readlines():
                widget.insert(tk.CURRENT, line)
            file.close()

        def save_then_quit():
            mode = 'x'
            if os.path.exists('data/output.txt'):
                mode = 'w'
            file_ = open('data/output.txt', mode)
            file_.write(widget.get('3.0', 'end'))
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", save_then_quit)

        sq = tk.Button(root, text="保存退出", command=save_then_quit)
        sq.pack(side='left')

        self.master.wait_window(root)

        self.my_controller.get_question_from_file()
        self.callback()
        self.master.update()
        self.my_controller.find_anwers()

    def open_file(self):
        self.save_file()

    def save_file(self):
        self.my_controller.close_all()

    def init_Operation_Menu(self):
        self.add_cascade(labe='操作', menu=self.operationMenu)
        operation_menu_label = ['搜索', '确认', '剔除']
        for label in operation_menu_label:
            self.operationMenu.add_command(label=label)
