# -*- coding:utf-8 -*-
__author__ = 'zach'
__create_time__ = '2015年12月20日17:48:10'

# Base: lib-detector/f5/st5.py
# Created at 2015/8/28
# Modified at 2015/8/28

import pymongo
import json


"""
    这么一段是把tgst5中的 package name 提取出来作为库的识别。
"""

def tgst5_to_pnset():
    pn_list = []
    tgst5 = open('tgst5.dat', 'r')
    for line in tgst5:
        package = json.loads(line)
        if "pn" in package:
            pn = package["pn"]
        else:
            pn = package["sp"]
        pn_list.append(pn)

    pnset = set(pn_list)

    #for pn in pnset:
    #    print pn

    return pnset

"""
    结束
"""

"""
    读取tagged_dict 得到 v - p 对
"""

def tagged_dict_to_vp():
    td = open('tagged_dict.txt', 'r')
    vp = {}
    for line in td:
        obj = json.loads(line)
        if "p" not in obj:
            continue
        vp[obj['v']] = obj['p']
    return vp

"""
    结束
"""

def run(pnset, vp):
    conn = pymongo.MongoClient('localhost', 27017)
    print "Mongo Connected"
    db = conn.get_database("lib-detect")
    package = db.get_collection("packages")


if __name__ == '__main__':
    pnset = tgst5_to_pnset()
    vp = tagged_dict_to_vp()
    run(pnset, vp)


"""
def main_func():
    print 'Mission Begin!'
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['lib-detect']
    d6 = db['d26']
    d0 = db['d20']

    res_num = open('st5_res_num.txt', 'w')

    cur_apk_num = 0
    cur_apk = ""
    cur_apk_list = []

    cnt = 0
    for d in d6.find().sort([("apk", pymongo.ASCENDING),("depth", pymongo.ASCENDING)]):
        if cnt % 10000 == 0:
            print cnt
        cnt += 1

        if d['apk'] != cur_apk:
            res_num.write(str(cur_apk_num))
            res_num.write('\n')
            cur_apk = d['apk']
            cur_apk_num = 0
            cur_apk_list = []
        if 'parent' in d:
            if d0.find({"path" : d['parent']}).count() == 0:
                continue
        cur_apk_list.append(d['path'])
        if '/'.join(d['path'].split('/')[:-1]) not in cur_apk_list:
            cur_apk_num += 1

    res_num.write(str(cur_apk_num))
    res_num.write('\n')
    res_num.close()

if __name__ == '__main__':
    main_func()"""

