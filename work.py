# -*- coding: utf-8 -*-
import MySQLdb
import re
import send
import resp

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


def new_user_step1(db, uid):
    send._pri_m('数据库中并没有查询到您的数据呢QAQ\n来注册一个吧', uid)
    send._pri_m('注册格式为: [您喜欢的名称] (保留方括号噢@A@)', uid)
    send._pri_m('尽量使用英文字母噢(*^_^*)', uid)
    return 'register'


def new_user_step2(db, uid, nn):
    cursor = db.cursor()
    try:
        command = "insert into users (" + "uid,nickname,level) values (" + str(
            uid) + ', ' + "\"" + str(nn) + "\"" + ', 1);'
        cursor.execute(command)
        db.commit()
        command = "insert into state (" + "uid,state) values (" + str(
            uid) + ', 0);'
        cursor.execute(command)
        db.commit()
    except Exception:
        db.rollback()
        send._pri_m('注册失败QAQ', uid)
        return 0
    send._pri_m('注册成功', uid)


def check_user(db, uid):
    cursor = db.cursor()
    command = 'select uid from users where uid=' + str(uid)
    cursor.execute(command)
    data = cursor.fetchone()
    if data:
        return 1
    else:
        return 0


def check_level(db, uid):
    cursor = db.cursor()
    command = 'select uid, level from users where uid=' + uid
    cursor.execute(command)
    data = cursor.fetchone()
    return data[1]


def oper(message_data):
    user_db = connect_db()
    type = message_data.get('post_type')
    if type == 'message':
        uid = message_data.get('user_id')
        message = message_data.get('message')
        exist = check_user(user_db, uid)
        matched = re.search(pattern=r"&#91;(.*?)&#93;",
                            string=message,
                            flags=re.M | re.I)
        if exist == 0:
            if matched is None:
                new_user_step1(user_db, uid)
                return 0
            else:
                new_user_step2(user_db, uid, matched.group(1))
                return 0
        if exist == 1:
            response = resp.get_response(message, uid)
            send._pri_m(response, uid)
        return 0
    else:
        if type == 'request':
            uid = message_data.get('user_id')
            flag = message_data.get('flag')
            send._acc_request(flag)
            return 0


if __name__ == '__main__':
    db = connect_db()
    uid = '1111111111'
    level = check_level(db, uid)
    print level
    # print data
