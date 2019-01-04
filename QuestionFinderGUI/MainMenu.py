import tkinter as tk


class MainMenu(tk.Menu):

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.operationMenu = tk.Menu(self, tearoff=0)
        self.fileMenu = tk.Menu(self, tearoff=0)
        # 初始化Menu
        self.initFileMenu()
        self.initOperationMenu()

    def initFileMenu(self):
        self.add_cascade(labe='文件', menu=self.fileMenu)
        file_menu_label = ['新建', '打开', '保存']
        for label in file_menu_label:
            self.fileMenu.add_command(label=label)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='关闭', command=self.master.quit)

    def initOperationMenu(self):
        self.add_cascade(labe='操作', menu=self.operationMenu)
        operation_menu_label = ['搜索', '确认', '剔除']
        for label in operation_menu_label:
            self.operationMenu.add_command(label=label)
