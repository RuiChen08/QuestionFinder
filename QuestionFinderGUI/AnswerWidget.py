import tkinter as tk
import webbrowser

width = 70
height = 10


class AnswerWidget:

    def __init__(self, frame, placement, number_of_widget):
        frame.place(relx=0, rely=placement / number_of_widget, relwidth=1, relheight=1 / 3)

        frame.update()

        self.link = None

        # set the content and import attributes
        self.widget = tk.Text(frame, width=width, height=height,
                              background='Gray', wrap='word')
        self.widget.place(x=0, y=0)
        self.widget.bind("<Control-KeyPress-o>", self.openLink)  # 重搜索的快捷键

        # open the link to the web
        button = tk.Button(frame, text="打开链接", command=self.openLink)
        button.place(x=220, y=120)

    def openLink(self):
        if not (self.link is None):
            webbrowser.get('safari').open(self.link)
