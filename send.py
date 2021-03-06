# -*- coding: utf-8 -*-
import requests
# import json


def _pri_m(str, goal):
    send = {'user_id': goal, 'message': str, 'auto_escape': False}
    api_url = 'http://127.0.0.1:5700/send_private_msg'
    requests.post(api_url, data=send)
    return 'SEND SUCCESSFULLY'


def _group_m(message, group, uid):
    mss = '[CQ:at,qq=%s] ' % str(uid) + message
    send = {'group_id': group, 'message': mss, 'auto_escape': False}
    api_url = 'http://127.0.0.1:5700/send_group_msg'
    requests.post(api_url, data=send)
    return 'SEND SUCCESSFULLY'


def _acc_request(flag):
    api_url = 'http://127.0.0.1:5700/set_friend_add_request'
    send = {'flag': flag, 'approve': True}
    requests.post(api_url, data=send)
    return 'SEND SUCCESSFULLY'


def _get_info():
    api_url = 'http://127.0.0.1:5700/get_login_info'
    data = requests.post(api_url)
    print data
    return data.get('user_id')
