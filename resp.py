# -*- coding: utf-8 -*-
import MySQLdb
import re
import random
import nmsl

host = 'localhost'
user = 'flask'
password = '123456'
database = 'bot'


def connect_db():
    db = MySQLdb.connect(host, user, password, database, charset='utf8')
    cursor = db.cursor()
    cursor.execute('select * from users')
    # data = cursor.fetchall()
    # print data
    return db


def get_state(uid):
    db = connect_db()
    cursor = db.cursor()
    command = 'select state from state where uid=' + str(uid) + ';'
    cursor.execute(command)
    data = cursor.fetchone()
    return data


def free(uid):
    db = connect_db()
    cursor = db.cursor()
    try:
        command = 'update state set state=' + '0' + ' where uid=' + str(
            uid) + ';'
        cursor.execute(command)
        db.commit()
    except Exception:
        db.rollback()


def dui_xian(uid):
    db = connect_db()
    cursor = db.cursor()
    try:
        command = 'update state set state=' + '1' + ' where uid=' + str(
            uid) + ';'
        cursor.execute(command)
        db.commit()
        return '你真的做好被骂的觉悟了吗？\n不道歉我可是不会停下来的噢'
    except Exception:
        db.rollback()
        return '别以为我说不过你，只是我今天不想骂人而已'


def mode_1_duixian(message, uid):
    pattern = re.compile(u'道歉')
    matched = re.search(pattern, message)
    if matched:
        try:
            free(uid)
            return '原谅你了'
        except Exception as e:
            print e
            return '你说什么我没听清ο(=•ω＜=)ρ⌒☆'
    pattern = re.compile(u'对不起')
    matched = re.search(pattern, message)
    if matched:
        try:
            free(uid)
            return '原谅你了'
        except Exception as e:
            print e
            return '你说什么我没听清ο(=•ω＜=)ρ⌒☆'
    res = nmsl.get()
    return res


def get_response(message, uid):  # 将回复处理按照优先级排列 根据关键词触发应用，同一个应用可能会有多个关键词触发
    state = get_state(uid)
    # state=1
    # 转移至对线模式
    if state[0] == 1:
        return mode_1_duixian(message, uid)
    # 以下是自由模式下所有的应用
    # state=0 自由模式
    print "\nmessage:", message
    # ---------
    # 改名
    # ---------
    pattern = r'&#91;(.*?)&#93;'
    matched = re.search(pattern, message)
    if matched:
        new_name = matched.group(1)
        return change_name(new_name, uid)
    # ---------
    # 自我介绍
    # ---------
    res = """我是Noir哟，由Navi开发的第一代基于 HTTP + Flask 的 QuneBot。详细信息可以在这里查看哦:https://navihx.github.io/2020/04/09/QQBot%E5%BC%80%E5%8F%91/\n"""
    pattern = re.compile(u'自我介绍')
    matched = re.search(pattern, message)
    if matched:
        return res
    pattern = re.compile(u'你是谁')
    matched = re.search(pattern, message)
    if matched:
        return res
    # ---------
    # 骰子
    # ---------
    pattern = re.compile(u'骰子')
    matched = re.search(pattern, message)
    if matched:
        pattern = re.compile(u'([0-9]*?)面')
        matched = re.search(pattern, message)
        if matched:
            return throwDice(int(matched.group(1)))
        else:
            return throwDice()
    # --------
    # 提问箱相关
    # --------
    """

    """
    # --------
    # 进入高强度对线
    # --------
    pattern = re.compile(u'nmsl')
    matched = re.search(pattern, message)
    if matched:
        return dui_xian(uid)
    pattern = re.compile(u'傻逼')
    matched = re.search(pattern, message)
    if matched:
        return dui_xian(uid)
    pattern = re.compile(u'你妈的')
    matched = re.search(pattern, message)
    if matched:
        return dui_xian(uid)
    pattern = re.compile(u'废物')
    matched = re.search(pattern, message)
    if matched:
        return dui_xian(uid)
    # --------
    # 默认回复
    # --------
    return "不好意思你在说什么我怎么听不懂QAQ"


# 骰子应用
def throwDice(num=6):
    if num != 6 and num != 20:
        return '抱歉，Noir还没有这种骰子呢（＞人＜；）'
    val = random.randint(1, int(num))
    return '+------+\n|   ' + str(val) + '   |\n+------+'


# 改名应用
def change_name(name, uid):
    db = connect_db()
    cursor = db.cursor()
    try:
        command = 'update users set nickname="' + str(
            name) + '" where uid=' + str(uid) + ';'
        cursor.execute(command)
        db.commit()
    except Exception:
        return "改名失败QAQ~"
    return "改名成功！"
