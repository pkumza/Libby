# -*- coding:utf-8 -*-
__author__ = 'zach'
__create_time__ = '2015年12月20日18:35:32'

import pymongo

def add_status_1():
    """
    建立索引
    status .ASCENDING
    :return: result string
    """
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['lib-detect']
    packages = db.get_collection('packages')
    result = packages.create_index([('apk', pymongo.ASCENDING),('depth', pymongo.ASCENDING)])
    print str(result)

if __name__ == '__main__':
    add_status_1()