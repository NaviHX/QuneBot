# -*- coding: utf-8 -*-
from flask import Flask, request
from json import loads
import work
# import re


bot_server = Flask(__name__)


@bot_server.route('/', methods=['POST'])
def server():
    data = request.get_data().decode('utf-8')
    data = loads(data)
    print data
    work.process(data)
    return ''


if __name__ == '__main__':
    bot_server.run(host='0.0.0.0', port=5701)
