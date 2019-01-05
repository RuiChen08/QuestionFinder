# -*- coding: utf-8 -*-

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
    default_message = "没有更多问题了"
    default_answer = ["问题为 \"没有更多问题了\", 此问题是无效问题", "请稍等，正在生成数据", "对不起，没有更多答案了"]

    def __init__(self, file=None):
        # Containing the question description, and its index
        self.questions = list()
        self.index_question = 0

        if file is None:
            file = "output.html"

        if os.path.exists(file):
            mode = 'w'
        else:
            mode = 'x'
        self.output_file = open(file, mode)

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
            return [self.default_answer[0]] * n  # "问题为 \"没有更多问题了\", 此问题是无效问题"

        hash_ = getHashing(question)

        if not (hash_ in self.Q_to_A.keys()):
            path = "data/" + hash_ + "candidate.csv"
            if not os.path.exists(path):
                Thread(target=lambda: self.find_answer_for_question_with_baidu(question)).start()
            return [self.default_answer[1]] * n  # "请稍等，正在生成数据"

        # dynamically change the cursor
        self.Q_to_AI[hash_] += n

        index = self.Q_to_AI[hash_]
        if (index >= 0) and (index <= len(self.Q_to_A[hash_])):
            answer = self.Q_to_A[hash_][index:index + abs(n)]
        else:
            if (index + 5 < 0) or (index - 5 > len(self.Q_to_A[hash_])):
                self.Q_to_AI[hash_] -= n
            answer = [self.default_answer[2]] * n  # "对不起，没有更多答案了"

        return answer

    def write_que_ans(self, question, answer, link):
        # self.output_file.write("<meta http - equiv = \"Content-Type\" content = \"text/html\"; charset=utf-8/>")
        self.output_file.write('<hr/>')
        self.output_file.write("<h1>" + question + "</h1>")
        for _ans in answer.split("\n\n"):
            index = _ans.find(':')
            if index == -1:
                self.output_file.write("<h3>" + _ans[0:] + "</h3>")
            else:
                self.output_file.write("<h2>" + _ans[0:index] + "</h2>")
                self.output_file.write("<h3>" + _ans[index + 1:] + "</h3>")
        self.output_file.write('<a href="%s" target="_blank">答案链接</a>' % link)
        self.output_file.flush()

    def close_all(self):
        self.output_file.close()
        suffix = 1
        while os.path.exists('data/output%d.txt' % suffix):
            os.system('rm data/output%d.txt' % suffix)
            suffix += 1

    def set_question_from_pictures(self, pic_dic):
        parent = os.listdir(pic_dic)

        suffix = 1
        for picture in parent:
            while os.path.exists('data/output%d.txt' % suffix):
                suffix += 1
            os.system('tesseract %s data/output%d -l chi-sim' % (os.path.join(pic_dic, picture), suffix))
            self.smart_modifying('data/output%d.txt' % suffix)

    def get_question_from_file(self):
        file = open('data/output.txt', 'r')

        self.__init__()

        ques_des = ""
        for line in file.readlines():
            line = line.strip()
            if line != "":
                ques_des += line
            else:
                if ques_des == "":
                    continue
                self.questions.append(ques_des.replace(' ', ''))
                ques_des = ""

        file.close()

    def find_anwers(self):
        for ques in self.questions:
            t = Thread(target=self.find_answer_for_question_with_baidu(ques))
            t.start()

    def smart_modifying(self, path):
        _file = open(path, 'r')
        ques = list()
        que = ""
        for line in _file.readlines():
            if line.strip() != "":
                if line.strip()[0].isdigit():
                    ques.append(que)
                    que = ""
            que += line

        ques.append(que)

        _file.close()
        _file = open(path, 'w')
        for que in ques:
            _file.write(que + "\n")


'''
    Following is the start-up part of of Question-Finder
'''


def printHelpMessage():
    print(" 用法: python controller -q descriptions [-u/d/ao/so] [args...]")
    print("    或者")
    print(" python controller -u url [-p/ao/so] [args...]")
    print("")
    print("其中选项包括:")
    print("   -f/F:<path/to/output/file>             指定输出文件的位置")
    print("   -p/P:<path/to/pictures/directory>      指定输出文件的位置")
    print("   -q/Q:<question description>            指定问题")
    print("   -u:<url link to answer>                指定用于搜索答案的链接")
    print("   -ao:<path to answer output file>       指定存放答案的文件")
    print("   -so:<path to answer output file>       指定存放搜索结果的文件")
    print("   -display[-d]                           用户交互界面")


# Controlling the flow by user's inputs
i = 1

os.system("export TESSDATA_PREFIX=/Users/chenrui/Projects/PyCharmProjects/QuestionFinder/TessOCR/tessdata")
if not os.path.exists('data'):
    os.mkdir('data')

# if the out file path is specified
if sys.argv[1] == '-f' or sys.argv[1] == '-F':
    con = Controller(sys.argv[2])
else:
    con = Controller()

GUI = False
while i < len(sys.argv):
    if sys.argv[i] == '-q' or sys.argv[i] == '-Q':
        con.questions.append(sys.argv[i + 1])
    elif sys.argv[i] == '-d' or sys.argv[i] == '-D' or sys.argv[i] == '-display':
        GUI = True
        i -= 1
    elif sys.argv[i] == '-p' or sys.argv[i] == '-P':
        con.set_question_from_pictures(sys.argv[i + 1])
    elif len(sys.argv) == 1 or sys.argv[1] == '-h':
        printHelpMessage()
        exit(0)
    elif len(sys.argv) == '-f' or sys.argv[1] == '-F':
        printHelpMessage()
        exit(0)
    i += 2

if GUI:
    MainWindow(con).start()
else:
    printHelpMessage()
