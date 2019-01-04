from tkinter import *
import pandas as pd
from QuestionFinderGUI.MainMenu import *
from QuestionFinderGUI.QuestionWidget import *
from QuestionFinderGUI.AnswerWidget import *


class MainWindow:

    def __init__(self, controller):
        # Create new window
        self.root = Tk()

        # Set my controller
        self.my_controller = controller

        # The container of text widgets
        self.answer_widgets = list()
        self.question_widgets = list()

        # The number of frames in each side
        self.number_of_question = 3
        self.number_of_answer = 5

        self.config_init()

    def config_init(self):
        # Q stand for Question
        self.root.title("QFinder")
        # Set the size of the window
        self.root.geometry("1000x800")

        # Add the main menu into root window
        main_menu = MainMenu(self.my_controller, self.root)
        self.root.config(menu=main_menu)

        # Create the frames of the main windows, left side for question description, right side for potential answers
        left_frame = Frame(self.root)
        left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        right_frame = Frame(self.root)
        right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        for i in range(self.number_of_answer):
            self.answer_widgets.append(AnswerWidget(Frame(right_frame), i, self.number_of_answer, self.my_controller))

        for i in range(self.number_of_question):
            self.question_widgets.append(QuestionWidget(Frame(left_frame), i, self.number_of_question,
                                                        self.answer_callback, self.my_controller))

    def answer_callback(self, answers, question=None):

        # clean the text box, showing the message "searching for answers now"
        for ans_box in self.answer_widgets:
            ans_box.widget.delete('1.0', 'end')
            ans_box.widget.insert(CURRENT, "请稍等,正在调取答案。。。")
            ans_box.widget.update()

        # Adding into text box
        for i in range(len(self.answer_widgets)):
            ans_box = self.answer_widgets[i]

            # Setting the answer
            if i < len(answers):
                answer = answers[i]
            else:
                # set it empty if there is no offered answer
                answer = ""

            # Deleting the so called 'searching' message
            ans_box.widget.delete('1.0', 'end')

            # Setting the question for ans_box
            if question is None:
                ans_box.question = None
            else:
                ans_box.question = question

            # Write the message into text box
            if answer == "":
                ans_box.widget.insert(CURRENT, "对不起，没有更多答案了")
            else:
                t_list = answer.split('\t')
                for a_ in t_list:
                    if a_.startswith('href:'):
                        ans_box.link = a_[a_.find('http'):]
                    else:
                        ans_box.widget.insert(CURRENT, a_ + '\n\n')

            # For testing
            # for name in answer.columns:
            #     for c in answer.index:
            #         if name == 'href':
            #             ans.link = answer[name][c]
            #         else:
            #             ans.widget.insert(CURRENT, name + ": " + answer[name][c] + "\n\n")
            #             ans.widget.update()

    def start(self):
        for que in self.question_widgets:
            que.set_new_question(self.my_controller.next_question())
        self.root.mainloop()