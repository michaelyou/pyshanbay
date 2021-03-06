#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""命令行下的扇贝词典
"""

import sys
import urlparse
from urllib2 import quote

import requests

from .shanbay import Shanbay, LoginException
from .utils import parse_settings
from .color import color



def check_error(func):
    u"""使用装饰器（decorator）处理异常."""
    def check(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LoginException:
            sys.exit(color('Login failed!', 'red', effect='underline'))
        except requests.exceptions.RequestException:
            sys.exit(color('Network trouble!', 'red', effect='underline'))
    return check


def encode(unicode_str, encoding=sys.stdout.encoding):
    return unicode_str.encode(encoding, 'ignore')


def decode(string, encoding=sys.stdin.encoding):
    return string.decode(encoding, 'ignore')


def output(msg):
    print encode(msg)


@check_error
def main():
    if sys.version_info[0] == 3:
        sys.exit(color("Sorry, this program doesn't support Python 3 yet",
                       'red', effect='underline'))
    settings = parse_settings()
    colour = settings.colour


    cmd_width = 55
    headers = {
        'Host': urlparse.urlsplit('http://www.shanbay.com/').netloc,
        'User-Agent': (' Mozilla/5.0 (Windows NT 6.2; rv:23.0) Gecko'
                       + '/20100101 Firefox/23.0'),
    }

    # 登录
    output('Login...')
    shanbay = Shanbay(settings.url_login, headers, settings.username,
                      settings.password)
    user_info = shanbay.get_user_info(settings.api_get_user_info)
    output('Welcome! %s.' % color(user_info.get('nickname'), colour))

    while True:
        word = quote(raw_input('Please input an english word: ').strip())
        if not word:
            continue

        # 输入 q 退出程序
        if word == 'q':
            output('Goodbye.')
            sys.exit(0)

        # 获取单词信息
        info = shanbay.get_word(settings.api_get_word, word)
        if not info:
            output("%s may not be an english word!" % color(word, colour))
            continue

        # 输出单词信息
        # 学习记录

        data = info.get('data')
        learning_id = data.get('learning_id')
        if not data:
            output("%s may not be an english word!" % color(word, colour))
            continue
        # 单词本身
        word = data.get('content')
        word_id = data.get('id')

        # 英文解释
        en_definitions = data.get('en_definitions')
        if en_definitions:
            en_definition = ['%s. %s' % (p, ','.join(d))
                             for p, d in en_definitions.iteritems()]
        else:
            en_definition = None
        # 中文解释
        cn_definition = data.get('definition')

        output(' %s '.center(cmd_width, '-') % color(word, colour,
                                                     effect='underline'))
        output('\nChinese definition:')
        output('%s' % cn_definition.strip())

        if settings.en_definition and en_definition:
            output('\nEnglish definition:')
            for en in en_definition:
                output('%s' % en.strip())


        # 例句
        examples = []
        if settings.example and learning_id:
            examples_info = shanbay.get_example(settings.api_get_example,
                                                learning_id)
            if examples_info:
                examples_dict = examples_info.get('examples')
                for example_dict in examples_dict:
                    #examples.append('%(first)s*%(mid)s*%(last)s'
                                    #'\n%(translation)s' % example_dict)
                    examples.append(
                        example_dict['first'] +
                        color(example_dict['mid'], colour) +
                        '%(last)s\n%(translation)s' % example_dict
                    )

        if examples:
            output('\nExamples:')
            for ex in examples:
                output('%s' % ex.strip())

        # 如果未收藏该单词
        if not learning_id:
            if settings.ask_add:
                ask = raw_input('Do you want to add %s to shanbay.com?'
                                ' (y/n): ' % color(word, colour))
                if ask.strip().lower().startswith('y'):
                    # 收藏单词
                    learning_id_info = shanbay.add_word(settings.api_add_word,
                                                        word_id)
                    learning_id = learning_id_info.get('data').get('id')
                    output('%s has been added to shanbay.com' % color(word,
                                                                      colour))
            elif settings.auto_add:
                learning_id_info = shanbay.add_word(settings.api_add_word,
                                                    word_id)
                learning_id = learning_id_info.get('id')
                output('%s has been added to shanbay.com' % color(word,
                                                                  colour))

        # 添加例句
        if learning_id and settings.ask_example:
            ask = raw_input('Do you want to add an example for '
                            'this word? (y/n): ')
            if ask.strip().lower().startswith('y'):
                while True:  # 支持多次添加例句
                    _break = False  # 是否跳槽循环
                    sentence = None
                    translation = None

                    # 例句
                    while not sentence:
                        sentence = raw_input('Please input sentence:\n')
                        if sentence.strip().lower() == 'q':
                            sentence = None
                            _break = True
                            break
                    if _break:
                        break

                    if sentence:
                        # 解释
                        while not translation:
                            translation = raw_input('Please input '
                                                    'translation:\n')
                            if translation.strip().lower() == 'q':
                                translation = None
                                _break = True
                                break
                    if _break:
                        break

                    # 添加例句到扇贝网
                    if sentence and translation:
                        sentence = sentence.strip()
                        translation = translation.strip()
                        encoding = sys.stdin.encoding
                        translation = translation.decode(encoding)
                        translation = translation.encode('utf8')

                        result = shanbay.add_example(settings.api_add_example,
                                                     word_id,
                                                     sentence,
                                                     translation)


                        status = result.get('msg')
                        if status == u'SUCCESS':
                            output('Add success')
                        elif status == u'FAILED':
                            output('Add Failed')


        else:
            pass

        output('-' * cmd_width)

if __name__ == '__main__':
    main()
