# -*- coding: utf-8 -*-
import re
import send
# import resp
import response
import database


def process(message_data):
    user_db = database.connect_db()
    type = message_data.get('post_type')
    message_type = message_data.get('message_type')
    if type == 'message' and message_type == 'private':
        uid = message_data.get('user_id')
        message = message_data.get('message')
        exist = database.check_user(uid, user_db)
        matched = re.search(pattern=r"&#91;(.*?)&#93;",
                            string=message,
                            flags=re.M | re.I)
        if exist == 0:
            if matched:
                database.user_register(uid, matched.group(1), user_db)
                return 0
            else:
                send._pri_m('数据库中并没有查询到您的数据呢QAQ\n来注册一个吧', uid)
                send._pri_m('注册格式为: [您喜欢的名称] (保留方括号噢@A@)', uid)
                send._pri_m('请尽量使用英文字母噢(*^_^*)', uid)
                return 0
        else:
            reply = response.reply(uid, type, message)
            data = reply.get_response()
            if data != 'ERROR':
                send._pri_m(data, uid)
            return 0
    elif type == 'message' and message_type == 'group':
        uid = message_data.get('user_id')
        gid = message_data.get('group_id')
        message = message_data.get('message')
        self_id = message_data.get('self_id')
        if not database.check_user(uid, user_db):
            stri = '数据库中并没有查询到您的数据呢QAQ\n来注册一个吧\n向机器人私聊发送消息完成注册'
            send._group_m(stri, gid, uid)
            return 0
        reply = response.group_reply(str(self_id), uid, type, message)
        data = reply.get_response()
        print data
        if data != 'ERROR':
            send._group_m(data, gid, uid)
        return 0
    elif type == 'requests':
        uid = message_data.get('user_id')
        flag = message_data.get('flag')
        send._acc_request(flag)
        return 0
