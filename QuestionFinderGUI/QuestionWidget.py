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
        self.widget.bind("<Button-1>", lambda e: self.displayFive())  # 展示答案的快捷键
        self.widget.bind("<Control-Shift-KeyPress-N>", lambda e: self.get_next_answers())  # 调取下五个答案的快捷键
        self.widget.bind("<Control-Shift-KeyPress-P>", lambda e: self.get_previous_answers())  # 调取之前五个答案的快捷键
        self.widget.bind("<Control-Shift-KeyPress-V>", lambda e: self.get_next_question())  # 重搜索的快捷键
        self.cur_q = ""

        search = tk.Button(frame, text="重新搜索", command=self.re_search_question)
        search.place(x=220, y=220)

        next = tk.Button(frame, text="下一题", command=self.get_next_question)
        next.place(x=280, y=220)

        next_a = tk.Button(frame, text="答案>>", command=self.get_next_answers)
        next_a.place(x=340, y=220)

        prev_a = tk.Button(frame, text="<<答案", command=self.get_previous_answers)
        prev_a.place(x=160, y=220)

    def set_new_question(self, description):
        # prev_q = self.cur_q
        self.cur_q = description
        self.widget.delete('1.0', 'end')
        self.widget.insert(tk.CURRENT, description)
        # return prev_q

    def get_next_question(self):
        # Get new question, and get it set
        n_q = self.my_controller.next_question()
        self.set_new_question(n_q)

        # Get the asnwer for these questions
        self.answer = self.my_controller.next_five_answers(self.cur_q)
        self.displayFive()

    def displayFive(self):
        # for debugging
        # print(event.widget)

        if hasattr(self.answer, "index") and hasattr(self.answer, "columns"):
            ans = []
            for c in self.answer.index:
                _a = ""
                for name in self.answer.columns:
                    _a += name + ":" + self.answer[name][c] + "\t"
                ans.append(_a)
            self.callback(ans, self)
        else:
            self.callback(self.answer, self)

    def get_next_answers(self):
        self.answer = self.my_controller.next_five_answers(self.cur_q)
        self.displayFive()

    def get_previous_answers(self):
        self.answer = self.my_controller.previous_five_answers(self.cur_q)
        self.displayFive()

    def re_search_question(self):
        self.cur_q = self.widget.get('1.0', 'end').strip()
        self.answer = self.my_controller.next_five_answers(self.cur_q)
        self.displayFive()

