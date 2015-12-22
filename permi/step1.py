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


def package_parent(package_name):
    return '/'.join(package_name.split('/')[:-1])


def run(pnset, vp):
    conn = pymongo.MongoClient('localhost', 27017)
    print "Mongo Connected"
    out = open('out.txt', 'w')
    db = conn.get_database("lib-detect")
    packages = db.get_collection("packages")
    # Init
    current_apk = ""
    path_dict = {}  # path 的 dict, key是 path， value是 状态 L代表lib， C代表custom code 的叶子， R代表不确定, T代表L的子节点
    dict_dict = {}  # api_dict 的 dict。 key是path， value是 package 的 api_dict
    lib_permission_call = 0
    # lib_permission_num = 0
    non_lib_permission_call = 0
    # non_lib_permission_num = 0

    # Loop
    cnt = 0
    for package in packages.find().sort([("apk", pymongo.ASCENDING), ("depth", pymongo.ASCENDING)]):
        # print package['path']
        if cnt % 1000 == 0:
            print cnt
        cnt += 1
        if current_apk != "" and current_apk != package['apk']:
            for path in path_dict:
                if path_dict[path] == 'L':
                    for api in dict_dict[path]:
                        api_num = int(api)
                        if api_num not in vp:
                            continue
                        lib_permission_call += len(vp[api_num]) * dict_dict[path][api]
                if path_dict[path] == 'C':
                    for api in dict_dict[path]:
                        api_num = int(api)
                        if api_num not in vp:
                            continue
                        non_lib_permission_call += len(vp[api_num]) * dict_dict[path][api]
            out.write(str(lib_permission_call)+',' + str(non_lib_permission_call) +'\n');

            # init
            lib_permission_call = 0
            non_lib_permission_call = 0
            path_dict.clear()
            dict_dict.clear()

        if package_parent(package['path']) in path_dict and path_dict[package_parent(package['path'])] == 'L':
            path_dict[package['path']] = 'T'
            continue
        if package_parent(package['path']) in path_dict and path_dict[package_parent(package['path'])] == 'T':
            path_dict[package['path']] = 'T'
            continue
        dict_dict[package['path']] = package['api_dict']
        for lib_package_name in pnset:
            if lib_package_name in package['path']:
                path_dict[package['path']] = 'L'
                break
        else:
            path_dict[package['path']] = 'C'        # 这个package人为是custom的（且为leaf）。
        if package_parent(package['path']) in path_dict:
            path_dict[package_parent(package['path'])] = 'R'    # 如果不是leaf，则定义为R。
        current_apk = package['apk']
    out.close()

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

