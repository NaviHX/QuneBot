# -*- coding: utf-8 -*-
import requests
# import json


def _pri_m(str, goal):
    send = {'user_id': goal, 'message': str, 'auto_escape': False}
    api_url = 'http://127.0.0.1:5700/send_private_msg'
    requests.post(api_url, data=send)
    return 'SEND SUCCESSFULLY'


def _acc_request(flag):
    api_url = 'http://127.0.0.1:5700/set_friend_add_request'
    send = {'flag': flag, 'approve': True}
    requests.post(api_url, data=send)
    return 'SEND SUCCESSFULLY'
