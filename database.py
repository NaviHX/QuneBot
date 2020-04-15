# -*- coding: utf-8 -*-
import MySQLdb
import json
import send
import io
file = io.open('setting.json', 'r', encoding='utf-8')
setting = json.load(file)
host = setting['database']['host']
user = setting['database']['user']
password = setting['database']['password']
database = setting['database']['db']


def connect_db():
    db = MySQLdb.connect(host, user, password, database, charset='utf8')
    return db


def check_user(uid, db):
    cursor = db.cursor()
    command = 'select uid from users where uid=' + str(uid)
    cursor.execute(command)
    data = cursor.fetchone()
    if data:
        return 1
    else:
        return 0


def check_level(uid, db):
    cursor = db.cursor()
    command = 'select uid, level from users where uid=' + uid
    cursor.execute(command)
    data = cursor.fetchone()
    return data[1]


def get_state(uid, db):
    cursor = db.cursor()
    command = 'select state from state where uid=' + str(uid) + ';'
    cursor.execute(command)
    data = cursor.fetchone()
    return data


def user_register(uid, name, db):
    cursor = db.cursor()
    try:
        command = "insert into users (" + "uid,nickname,level) values (" + str(
            uid) + ', ' + "\"" + str(name) + "\"" + ', 1);'
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


def change_name(uid, name, db):
    cursor = db.cursor()
    try:
        command = 'update users set nickname="' + str(
            name) + '" where uid=' + str(uid) + ';'
        cursor.execute(command)
        db.commit()
    except Exception:
        return "改名失败QAQ~"
    return "改名成功！"


def change_state(uid, state, db):
    cursor = db.cursor()
    try:
        command = 'update state set state=' + str(state) + ' where uid=' + str(
            uid) + ';'
        cursor.execute(command)
        db.commit()
    except Exception:
        db.rollback
        return 0
    return 1
