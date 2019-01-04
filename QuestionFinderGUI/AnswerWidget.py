import tkinter as tk
import webbrowser

width = 70
height = 10


class AnswerWidget:
    def __init__(self, frame, placement, number_of_widget, controller):
        frame.place(relx=0, rely=placement / number_of_widget, relwidth=1, relheight=1 / 3)

        frame.update()

        # Setting the controller
        self.my_controller = controller

        # set the content and important attributes

        self.widget = tk.Text(frame, width=width, height=height,
                              background='Gray', wrap='word')
        self.widget.place(x=0, y=0)
        self.widget.bind("<Control-KeyPress-o>", self.openLink)  # 重搜索的快捷键

        # Setting the link which represent the link to potential answers
        self.link = None

        # open the link to the web
        button = tk.Button(frame, text="打开链接", command=self.openLink)
        button.place(x=220, y=120)

        select = tk.Button(frame, text="选择答案", command=self.writeAnswer)
        select.place(x=280, y=120)

    def openLink(self):
        if not (self.link is None):
            webbrowser.get('safari').open(self.link)

    def writeAnswer(self):
        if not (self.widget.get('1.0', 'end').strip() == "对不起，没有更多答案了"):
            self.my_controller.write_que_ans("test question", "test answer")