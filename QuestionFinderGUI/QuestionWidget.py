import tkinter as tk

width = 70
height = 17


class QuestionWidget:

    def __init__(self, frame, placement, number_of_widget, callback, controller):
        # Store the previous question

        # Place the frame according to the ranking
        frame.place(relx=0, rely=placement / number_of_widget, relwidth=1, relheight=1 / 3)

        # callback function for displaying answers
        self.callback = callback
        self.my_controller = controller

        # Place the widgets into frame, and config them
        self.widget = tk.Text(frame, width=width, height=height,
                              background='Gray', wrap='word')
        self.widget.place(x=0, y=0)

        # place to store the answer
        self.answer = list()
        self.widget.bind("<Button-1>", self.displayFive)  # 展示答案的快捷键
        self.widget.bind("<Control-Shift-KeyPress-N>", self.displayNewFive)  # 重搜索的快捷键
        self.widget.bind("<Control-Shift-KeyPress-P>", self.getPreviousAnswers)  # 重搜索的快捷键
        self.widget.bind("<Control-Shift-KeyPress-V>", self.get_next_question)  # 重搜索的快捷键
        self.cur_q = ""

        search = tk.Button(frame, text="重新搜索", command=lambda: self.displayNewFive(0))
        search.place(x=220, y=220)

        next = tk.Button(frame, text="下一题", command=lambda: self.get_next_question(0))
        next.place(x=280, y=220)

        next_a = tk.Button(frame, text="答案>>", command=lambda: self.displayNewFive(0))
        next_a.place(x=340, y=220)

        prev_a = tk.Button(frame, text="<<答案", command=lambda: self.getPreviousAnswers(0))
        prev_a.place(x=160, y=220)

    def set_new_question(self, description):
        prev_q = self.cur_q
        self.cur_q = description
        self.widget.delete('1.0', 'end')
        self.widget.insert(tk.CURRENT, description)
        return prev_q

    def get_next_question(self, event):
        n_q = self.my_controller.next_question()
        self.answer = []
        self.callback(self.answer)
        self.set_new_question(n_q)
        if not (n_q == "没有更多问题了"):
            self.displayFive(event)

    def displayFive(self, event):
        # for debugging
        # print(event.widget)

        ans = list()
        # For testing

        if (not (self.answer is None)) and (type(self.answer) == list):
            self.callback([])
            self.answer = self.my_controller.next_five_answers(self.cur_q)

        if self.answer is None:
            self.callback(ans)
            return

        if type(self.answer) == list:
            self.callback(self.answer)
            return

        for c in self.answer.index:
            _a = ""
            for name in self.answer.columns:
                _a += name + ":" + self.answer[name][c] + "\t"
            ans.append(_a)

        # self.widget.cur_q = self.widget.get('1.0', 'end').strip()
        self.callback(ans)

    def displayNewFive(self, event):
        self.answer = []
        self.cur_q = self.widget.get('1.0', 'end').strip()
        self.displayFive(event)

    def getPreviousAnswers(self, event):
        self.callback([])
        self.answer = self.my_controller.previous_five_answers(self.cur_q)
        self.displayFive(event)
