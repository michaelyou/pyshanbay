#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""一些功能函数
"""

import os
from getpass import getpass

from .cmdoption import CmdOption
from .conf import Settings


# Modified from https://github.com/webpy/webpy/blob/master/web/utils.py
class Storage(dict):

    """A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.

    >>> o = storage(a=1)
    >>> o.a
    1
    >>> o['a']
    1
    >>> o.a = 2
    >>> o['a']
    2
    >>> del o.a
    >>> o.a
    Traceback (most recent call last):
    ...
    AttributeError: 'a'

    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'

storage = Storage


def parse_settings():
    u"""解析各个设置项."""
    # 获取各命令行参数的值
    options = CmdOption().options
    configfile = options.settings
    username = options.username
    password = options.password
    ask_add_example = options.ask_add_example
    example = options.example
    english = options.english

    # 读取配置文件
    if configfile:
        configfile = os.path.realpath(configfile)
    conf = Settings(configfile, username, '').settings

    if password is None:
        password = conf.password
        if not password:
            password = getpass('Please input password: ')
    username = username or conf.username
    password = password or conf.password


    settings = {}
    # shanbay.com
    #site = conf.site
    site = 'http://www.shanbay.com/'
    settings['site'] = 'http://www.shanbay.com/'
    settings['username'] = username
    settings['password'] = password
    settings['auto_add'] = conf.auto_add  # 自动保存单词到扇贝网
    settings['ask_add'] = conf.ask_add  # 询问是否保存单词
    if english is None:
        english = conf.enable_en_definition
    settings['en_definition'] = english  # 单词英文释义
    #settings['url_login'] = site + conf.url_login
    settings['url_login'] = conf.url_login
    settings['api_get_word'] = conf.api_get_word  # 获取单词信息的 api
    settings['api_get_example'] = conf.api_get_example  # 获取例句的 api
    settings['api_add_word'] = conf.api_add_word  # 保存单词的 api
    # 获取用户信息的 api
    settings['api_get_user_info'] = conf.api_get_user_info
    settings['api_add_example'] = conf.api_add_example  # 添加例句的 api
    if ask_add_example is None:
        ask_add_example = conf.ask_add_example  # 询问是否添加例句
    settings['ask_example'] = ask_add_example
    if example is None:
        example = conf.enable_example
    settings['example'] = example  # 用户自己添加的单词例句


    settings['colour'] = options.colour

    return storage(settings)
