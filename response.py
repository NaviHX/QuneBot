# -*- coding: utf-8 -*-
import database
import re
import nmsl
import random


# 骰子应用
def throwDice(num=6):
    if num != 6 and num != 20 and num != 12:
        return '抱歉，Noir还没有这种骰子呢（＞人＜；）'
    val = random.randint(1, int(num))
    return '+------+\n|   ' + str(val) + '   |\n+------+'


def mode_1_duixian(message, uid):
    db = database.connect_db()
    pattern = re.compile(u'道歉')
    matched = re.search(pattern, message)
    if matched:
        try:
            database.change_state(uid, 0, db)
            return '原谅你了'
        except Exception as e:
            print e
            return '你说什么我没听清ο(=•ω＜=)ρ⌒☆'
    pattern = re.compile(u'对不起')
    matched = re.search(pattern, message)
    if matched:
        try:
            database.change_state(uid, 0, db)
            return '原谅你了'
        except Exception as e:
            print e
            return '你说什么我没听清ο(=•ω＜=)ρ⌒☆'
    res = nmsl.get()
    return res


def get_response(uid, message):
    db = database.connect_db()
    state = database.get_state(str(uid), db)
    print state
    # state=1
    # 转移至对线模式
    if state[0] == 1:
        return mode_1_duixian(message, uid)
    # state=0 自由模式
    # ---------
    # 改名
    # ---------
    matched = re.search(pattern=r"&#91;(.*?)&#93;", string=message, flags=re.M | re.I)
    if matched:
        new_name = matched.group(1)
        return database.change_name(uid, new_name, db)  # 直接在数据库中更改
    # ---------
    # 骰子
    # ---------
    list = [u'骰子']
    for key in list:
        pattern = re.compile(key)
        matched = re.search(pattern, message)
        if matched:
            pattern = re.compile(u'([0-9]*?)面')
            matched = re.search(pattern, message)
            if matched:
                return throwDice(int(matched.group(1)))
            else:
                return throwDice()
    # --------
    # 进入高强度对线
    # --------
    list = [u'nmsl', u'傻逼', u'废物', u'你妈的']
    for key in list:
        pattern = re.compile(key)
        matched = re.search(pattern, message)
        if matched:
            db = database.connect_db()
            if database.change_state(uid, 1, db):
                return '你真的做好被骂的觉悟了吗？\n不道歉我可是不会停下来的噢'
            else:
                return '别以为我说不过你，只是我今天不想骂人而已'
    # --------
    # 默认回复
    # --------
    return "不好意思你在说什么我怎么听不懂QAQ"
