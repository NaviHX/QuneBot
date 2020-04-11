# -*- coding: utf-8 -*-
import requests


def get():
    try:
        html = requests.get('https://nmsl.shadiao.app/api.php').text
    except Exception as e:
        print e
        return '{{{(>_<)}}}完了，这下骂不赢了'
    return html


if __name__ == '__main__':
    print get()
