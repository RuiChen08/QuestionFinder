import os
import sys
from threading import Thread

import pandas
from QuestionFinderGUI.MainWindow import MainWindow
from hashlib import md5


def getHashing(string):
    md = md5()
    md.update(string.encode('utf8'))
    return md.hexdigest()


class Controller:

    default_message="没有更多问题了"

    def __init__(self):
        # Containing the question description, and its index
        self.questions = list()
        self.index_question = 0

        # Mapping from question to its answer, and its answer's index
        self.Q_to_A = {}
        self.Q_to_AI = {}

    def next_question(self):
        self.index_question += 1
        if len(self.questions) < self.index_question:
            return self.default_message
        return self.questions[self.index_question - 1]

    def find_answer_for_question_with_baidu(self, que):
        hash_ = getHashing(que)
        path = "data/" + hash_ + "candidate.csv"

        if not os.path.exists(path):
            # using Baidu spider find finding all potential answer for this question
            os.system("scrapy crawl baidu -a question_url=\"" + que + "\" -o " + path)
            print("\n\npotential answers are stored in", path)
        self.Q_to_A[hash_] = pandas.read_csv(path)
        self.Q_to_AI[hash_] = -5

    def clean_question(self, no_needed_quq):
        hash_ = getHashing(no_needed_quq)
        path = "data/" + hash_ + "candidate.csv"

        # clean if exist
        if no_needed_quq in self.Q_to_A.keys():
            self.Q_to_A.pop(hash_)
            self.Q_to_AI.pop(hash_)
            os.system("rm " + path)

    def next_five_answers(self, question):
        return self.next_n_answer(question, 5)

    def previous_five_answers(self, question):
        return self.next_n_answer(question, -5)

    def next_n_answer(self, question, n):
        if (question == self.default_message):
            return [""] * n

        hash_ = getHashing(question)

        if not (hash_ in self.Q_to_A.keys()):
            path = "data/" + hash_ + "candidate.csv"
            if not os.path.exists(path):
                Thread(target=lambda: self.find_answer_for_question_with_baidu(question)).start()
            return ["请稍等，正在生成数据"] * n

        # dynamically change the cursor
        self.Q_to_AI[hash_] += n

        index = self.Q_to_AI[hash_]
        if (index >= 0) and (index <= len(self.Q_to_A[hash_])):
            answer = self.Q_to_A[hash_][index:index+abs(n)]
        else:
            if (index + 5 < 0) or (index - 5 > len(self.Q_to_A[hash_])):
                self.Q_to_AI[hash_] -= n
            answer = None

        return answer


'''
    Following is the start-up part of of Question-Finder
'''


def printHelpMessage():
    print(" 用法: python controller -q descriptions [-u/d/ao/so] [args...]")
    print("    或者")
    print(" python controller -u url [-p/ao/so] [args...]")
    print("")
    print("其中选项包括:")
    print("   -q:<question description>              指定问题")
    print("   -u:<url link to answer>                指定用于搜索答案的链接")
    print("   -ao:<path to answer output file>       指定存放答案的文件")
    print("   -so:<path to answer output file>       指定存放搜索结果的文件")
    print("   -display[-d]                           用户交互界面")


# Controlling the flow by user's inputs
i = 1
con = Controller()
GUI = False
while i < len(sys.argv):
    if sys.argv[i] == '-q' or sys.argv[i] == '-Q':
        con.questions.append(sys.argv[i + 1])
    elif sys.argv[i] == '-d' or sys.argv[i] == '-D' or sys.argv[i] == '-display':
        GUI = True
        i -= 1
    elif len(sys.argv) == 1 or sys.argv[1] == '-h':
        printHelpMessage()
        exit(0)
    i += 2

if len(con.questions) != 0:
    for ques in con.questions:
        t2 = Thread(target=con.find_answer_for_question_with_baidu, args=(ques,))
        t2.start()
    if GUI:
        MainWindow(con).start()
else:
    printHelpMessage()
