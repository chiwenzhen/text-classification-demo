# coding=utf-8
import re
from myutils import TopkHeap
import time
import numpy as np
from collections import defaultdict

def add_n_to_file():
    file_num = 19178
    for i in range(1, file_num):
        num = [0, 0, 0, 0]
        with open("article15081608/attr/" + str(i), "r") as file_input:
            lines = file_input.readlines()
            line_num = len(lines)
            if 0 < line_num < 5:
                num[line_num - 1] += 1
            else:
                print "article15081608/attr/" + str(i) + ": " + str(line_num) + "行"
    print "一行：" + str(num[0])
    print "二行：" + str(num[1])
    print "三行：" + str(num[2])
    print "四行：" + str(num[3])

        # with open("article15081608/attr/" + str(i), "a") as file_output:
        #     file_output.write("\n")
        # with open("article15081608/attr/" + str(i), "r") as file_input:
        #     lines = file_input.readlines()
        #     line_num = len(lines)
        #     if 0 < line_num < 5:
        #         num[line_num - 1] += 1
        #     else:
        #         print "article15081608/attr/" + str(i) + ": " + str(line_num) + "行"
        # print "一行：" + str(num[0])
        # print "二行：" + str(num[1])
        # print "三行：" + str(num[2])
        # print "四行：" + str(num[3])

def norm_html():
    with open("tomjerry.html", "r") as file:
        html = file.read()
        # html = "\"tomjerry/bootstrap.min.css\""

        stan = "\"{{ url_for('static', filename='myresources1/bootstrap.min.css') }}\""
        new_html = re.sub(r"\"tomjerry/(.*?)\"",
                          "\"{{ url_for('static', filename='myresources1/\g<1>') }}\"", html)

        print stan == new_html
        print stan
        print new_html

        with open("tomjerry_new.html", "w") as fileo:
            fileo.write(new_html)

def read_file_test():
    with open("a.txt", "r") as file:
        print file.readline()
        print file.readline()

        for line in file.readlines():
            print line

def split_corpus():
    corpus_name = "article15081608" + "/seg_join/corpus.txt"
    corpus_train_name = "article15081608" + "/seg_join/corpus_train.txt"
    corpus_test_name = "article15081608" + "/seg_join/corpus_test.txt"
    with open(corpus_name, "r") as corpus_file:
        pass

def set_test():
    stopword = set([u"直播", u"VR", u"人工智能"])
    print u"直播" in stopword
    print u"VR" in stopword


def tree():
    return defaultdict(tree)


if __name__ == "__main__":
    from treelib import Node, Tree
    tree = Tree()
    tree.create_node("Harry", -1)  # root node
    tree.create_node("Jane", 2, parent=-1)
    tree.create_node("Bill", 3, parent=-1)
    tree.create_node("Diane", 4, parent=2)
    tree.create_node("Mary", 5, parent=4)
    tree.create_node("Mark", 6, parent=2)
    tree.show()



