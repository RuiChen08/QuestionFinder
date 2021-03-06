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
        self.widget.bind("<Control-KeyPress-o>", self.open_Link)  # 重搜索的快捷键

        # Setting the link which represent the link to potential answers
        self.link = None

        # which should be the questioner of current answer
        self.questioner = None

        # open the link to the web
        button = tk.Button(frame, text="打开链接", command=self.open_Link)
        button.place(x=220, y=120)

        select = tk.Button(frame, text="选择答案", command=self.write_Answer)
        select.place(x=380, y=120)

    def open_Link(self):
        if not (self.link is None):
            webbrowser.get('safari').open(self.link)

    def write_Answer(self):
        answer = self.widget.get('1.0', 'end').strip()
        if not ((answer in self.my_controller.default_answer) or (self.questioner is None)):
            self.my_controller.write_que_ans(self.questioner.cur_q, answer, self.link)
            self.questioner.get_next_question()