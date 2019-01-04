import tkinter as tk


class MainMenu(tk.Menu):

    def __init__(self, controller, master=None, cnf={}, **kw):

        # Settle it out
        super().__init__(master, cnf, **kw)
        self.operationMenu = tk.Menu(self, tearoff=0)
        self.fileMenu = tk.Menu(self, tearoff=0)

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

    def quit(self):
        self.save_file()
        self.master.quit()

    def create_new(self):
        self.save_file()

    def open_file(self):
        self.save_file()

    def save_file(self):
        self.my_controller.close_all()

    def init_Operation_Menu(self):
        self.add_cascade(labe='操作', menu=self.operationMenu)
        operation_menu_label = ['搜索', '确认', '剔除']
        for label in operation_menu_label:
            self.operationMenu.add_command(label=label)


