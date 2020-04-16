# -*- coding: utf-8 -*-
from xpinyin import Pinyin
import random
p = Pinyin()


def init(uid):
    file = open('./idiom_state/' + str(uid) + '.st', 'w')
    file.write(u'0')
    file.close()


def get_next(word, uid):
    pinyin = p.get_pinyin(word[-1], convert='upper')
    file = open('idioms/' + pinyin[0], 'r')
    base = file.readlines()
    random.shuffle(base)
    for i in base:
        i = i.decode('utf-8')
        temp = p.get_pinyin(i[0], convert='upper')
        if temp == pinyin and i[:-1] != word:
            with open('./idiom_state/' + str(uid) + '.st', 'w') as file:
                answer = p.get_pinyin(i[-2], convert='upper')
                print answer
                file.write(answer.encode('utf-8'))
            return i[:-1]
    return None


def check_answer(word, uid):
    temp = p.get_pinyin(word[0:1], convert='upper')
    with open('./idiom_state/' + str(uid) + '.st', 'r+') as file:
        std = file.readline()
        print std
        print temp
        if std == '0':
            return 1
        if std == temp:
            return 1
        else:
            return 0


if __name__ == '__main__':
    print get_next(u'有一说一', 0)
