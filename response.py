# -*- coding: utf-8 -*-
import database
import re
import nmsl
import random
import json
import io
import idiom


# 骰子应用
def throwDice(num=6):
    if num != 6 and num != 20 and num != 12:
        return '抱歉，Noir还没有这种骰子呢（＞人＜；）'
    val = random.randint(1, int(num))
    return '+------+\n|   ' + str(val) + '   |\n+------+'


class reply:
    uid = 0
    post_type = ''
    message = ''
    setting = ''

    def __init__(self, uid, post_type, message):
        self.uid = uid
        self.post_type = post_type
        self.message = message
        file = io.open('setting.json', 'r', encoding='utf-8')
        self.setting = json.load(file)

    def __del__(self):
        print '回复结束'

    def check(self):
        return 1

    def throwDice(num=6):
        if num != 6 and num != 20 and num != 12:
            return '抱歉，Noir还没有这种骰子呢（＞人＜；）'
        val = random.randint(1, int(num))
        return '+------+\n|   ' + str(val) + '   |\n+------+'

    def mode_1_duixian(self):
        db = database.connect_db()
        pattern = re.compile(u'道歉')
        matched = re.search(pattern, self.message)
        if matched:
            try:
                database.change_state(self.uid, 0, db)
                return '原谅你了'
            except Exception as e:
                print e
                return '你说什么我没听清ο(=•ω＜=)ρ⌒☆'
        pattern = re.compile(u'对不起')
        matched = re.search(pattern, self.message)
        if matched:
            try:
                database.change_state(self.uid, 0, db)
                return '原谅你了'
            except Exception as e:
                print e
            return '你说什么我没听清ο(=•ω＜=)ρ⌒☆'
        res = nmsl.get()
        return res

    def mode_2_idiom(self):
        pattern = re.compile(u'#')
        matched = re.search(pattern, self.message)
        if matched:
            db = database.connect_db()
            database.change_state(self.uid, 0, db)
            return '不想玩了吗？那就结束吧ヾ(≧▽≦*)o'
        if idiom.check_answer(self.message, self.uid):
            try:
                gg = random.randint(1, 4)
                if gg == 4:
                    db = database.connect_db()
                    database.change_state(self.uid, 0, db)
                    return '这是啥呀？我认输还不行吗o((>ω< ))o'
                ret = idiom.get_next(self.message, self.uid)
                if ret is None:
                    db = database.connect_db()
                    database.change_state(self.uid, 0, db)
                    return '这是啥呀？我认输还不行吗o((>ω< ))o'
                return ret
            except Exception:
                db = database.connect_db()
                database.change_state(self.uid, 0, db)
                return '这是啥呀？我认输还不行吗o((>ω< ))o'
        else:
            gg = random.randint(1, 3)
            print gg
            if gg == 3:
                db = database.connect_db()
                database.change_state(self.uid, 0, db)
                return '乱接可是不对的哟，现在游戏结束'
            else:
                return '再给你一个机会吧'

    def get_response(self):
        if not self.check():
            return 'ERROR'
        db = database.connect_db()
        state = database.get_state(str(self.uid), db)
        print state
        # -----------------------------------------------------
        # state=1
        # 转移至对线模式
        if state[0] == 1:
            return self.mode_1_duixian()
        # -----------------------------------------------------
        # state=2
        # 成语接龙模式
        if state[0] == 2:
            return self.mode_2_idiom()
        # -----------------------------------------------------
        # state=0 自由模式
        # ---------
        # 自我介绍
        # ---------
        res = """我是Noir哟，由Navi开发的第一代基于 HTTP + Flask 的 QuneBot。详细信息可以在这里查看哦:https://navihx.github.io/2020/04/09/QQBot%E5%BC%80%E5%8F%91/\n"""
        pattern = re.compile(u'自我介绍')
        matched = re.search(pattern, self.message)
        if matched:
            return res
        pattern = re.compile(u'你是谁')
        matched = re.search(pattern, self.message)
        if matched:
            return res
        # ---------
        # 改名
        # ---------
        matched = re.search(pattern=r"&#91;(.*?)&#93;",
                            string=self.message,
                            flags=re.M | re.I)
        if matched:
            new_name = matched.group(1)
            return database.change_name(self.uid, new_name, db)  # 直接在数据库中更改
        # ---------
        # 骰子
        # ---------
        list = [u'骰子']
        for key in list:
            pattern = re.compile(key)
            matched = re.search(pattern, self.message)
            if matched:
                pattern = re.compile(u'([0-9]*?)面')
                matched = re.search(pattern, self.message)
                if matched:
                    return throwDice(int(matched.group(1)))
                else:
                    return throwDice()
        # --------
        # 进入高强度对线
        # --------
        if self.setting['nmsl']['on']:
            list = self.setting['nmsl']['key']
            for key in list:
                pattern = re.compile(key)
                matched = re.search(pattern, self.message)
                if matched:
                    db = database.connect_db()
                    if database.change_state(self.uid, 1, db):
                        return '你真的做好被骂的觉悟了吗？\n不道歉我可是不会停下来的噢'
                    else:
                        return '别以为我说不过你，只是我今天不想骂人而已'
        # --------
        # 成语接龙
        # --------
        if self.setting['idiom']['on']:
            list = self.setting['idiom']['key']
            for key in list:
                pattern = re.compile(key)
                matched = re.search(pattern, self.message)
                if matched:
                    db = database.connect_db()
                    if database.change_state(self.uid, 2, db):
                        idiom.init(self.uid)
                        return '那就一起来玩成语接龙吧'
                    else:
                        return '今天不是很想玩呢'
        # --------
        # 默认回复
        # --------
        return "不好意思你在说什么我怎么听不懂QAQ"


class group_reply(reply):
    sid = ''

    def __init__(self, self_id, uid, post_type, message):
        self.uid = uid
        self.post_type = post_type
        self.message = message
        self.sid = self_id
        file = io.open('setting.json', 'r', encoding='utf-8')
        self.setting = json.load(file)

    def check(self):
        pattern = re.compile('CQ:at,qq=([0-9]*?)]')
        print self.message
        matched = re.search(pattern, self.message)
        if matched:
            uid = matched.group(1)
            sid = self.sid.strip()
            uid = uid.strip()
            if uid == sid:
                mlist = self.message.split()
                self.message = mlist[1]
                print self.message
                return 1
        return 0
