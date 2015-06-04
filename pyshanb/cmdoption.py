#Parse!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
处理命令行参数
"""

from argparse import ArgumentParser

from .__init__ import __version__
from .conf import default_configfile


class CmdOption(object):
    def __init__(self):
        self.version = 'PyShanb %s' % __version__
        description = 'An command line tool for shanbay.com.'
        self.parser = ArgumentParser(description=description)

        self.parser.add_argument('-V', '--version', action='version',
                                 version=self.version)
        self.parser.add_argument('-s', '--settings', dest='settings',
                                 help='the settings file of the application',
                                 default=default_configfile)
        self.parser.add_argument('-u', '--username', dest='username',
                                 help='the account username of shanbay.com')
        self.parser.add_argument('-p', '--password', dest='password',
                                 help='the account password of shanbay.com')

        group_example = self.parser.add_mutually_exclusive_group()
        group_example.add_argument('-e', '--add-example', action='store_true', default=None,
                                   dest='ask_add_example',
                                   help='enable "Add example" feature')
        group_example.add_argument('-E', '--disable-add-example', action='store_false', default=None,
                                   dest='ask_add_example',
                                   help='disable "Add example" feature')


        self.parser.add_argument('--color', dest='colour', default='green',
                                 choices=['black', 'white', 'red', 'green',
                                          'yellow', 'blue', 'magenta', 'cyan',
                                          'gray'],
                                 help='colorize keyword (default: green)')


        group_ex = self.parser.add_mutually_exclusive_group()
        group_ex.add_argument('--example', '--enable-example', action='store_true',
                              dest='example', help='enable examples',
                              default=None)
        group_ex.add_argument('--disable-example', action='store_false',
                              dest='example', help='disable examples',
                              default=None)

        group_en = self.parser.add_mutually_exclusive_group()
        group_en.add_argument('--english', action='store_true',
                              dest='english', help='enable english definition',
                              default=None)
        group_en.add_argument('--disable-english', action='store_false',
                              dest='english', help='disable english definition',
                              default=None)

        self.options = self.parser.parse_args()


def main():
    options = CmdOption().options
    print 'settings: ', options.settings
    print 'username: ', options.username
    print 'password: ', options.password
    print 'ask_add_example: ', options.ask_add_example
    print 'enable_iciba: ', options.enable_iciba
    print 'auto_play: ', options.auto_play
    print 'color: ', options.colour
    print 'example: ', options.example
    print 'english: ', options.english

if __name__ == '__main__':
    main()
