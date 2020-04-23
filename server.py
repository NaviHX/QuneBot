# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, render_template
from json import loads, dumps, load
import work
from database import check_admin, get_users
import send
import io

bot_server = Flask(__name__)


@bot_server.route('/', methods=['POST', 'GET'])
def server():
    if request.method == 'POST':
        data = request.get_data().decode('utf-8')
        data = loads(data)
        print data
        work.process(data)
        return ''
    else:
        return redirect(url_for("admin"))


@bot_server.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        pwd = request.form['pwd']
        data = get_users()
        if check_admin(pwd):
            file = io.open('setting.json', 'r')
            setting = load(file)
            setting = dumps(setting,
                            sort_keys=True,
                            indent=4,
                            separators=(',', ':'))
            return render_template("admin.html", list=data, setting=setting)
        else:
            return render_template("login.html")


@bot_server.route('/group_send', methods=['POST'])
def group_send():
    message = request.form['message']
    list = get_users()
    for user in list:
        uid = user[0]
        send._pri_m(message, uid)
    data = get_users()
    file = io.open('setting.json', 'r')
    setting = load(file)
    setting = dumps(setting, sort_keys=True, indent=4, separators=(',', ':'))
    return render_template("admin.html", list=data, setting=setting)


if __name__ == '__main__':
    if check_admin(None):
        bot_server.run(host='0.0.0.0', port=5701)
    else:
        print "WRONG PASSWORD"
