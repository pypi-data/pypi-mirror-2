#coding:utf-8

from os.path import abspath, dirname, join, normpath
import sys

#初始化python的查找路径
PREFIX = normpath(dirname(dirname(dirname(abspath(__file__)))))
if PREFIX not in sys.path:
    sys.path = [PREFIX] + sys.path

