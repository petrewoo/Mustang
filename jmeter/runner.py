#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import os
import argparse
from ConfigParser import SafeConfigParser
from subprocess import call
from time import time


BASE_DIR=os.path.dirname(os.path.abspath(__file__))
CONF_FILE=os.path.join(BASE_DIR, 'config.ini')


class JmeterPathInvalid(Exception):
    pass


class ThreadConfInvalid(Exception):
    pass


def get_conf(fn):
    config = SafeConfigParser()
    config.read(fn)

    jmeter_path = config.get('conf', 'jmeter', None)
    if not jmeter_path:
        raise JmeterPathInvalid

    threads = config.get('conf', 'threads', None)
    if not threads:
        raise ThreadConfInvalid

    threads_list = list(threads.split(','))

    return jmeter_path, threads_list


def get_args():
    """This function using jmeter execute testcase background."""

    parser = argparse.ArgumentParser('Jmeter runner arguments.')
    parser.add_argument('duration', help='how long execute test case',
                        type=str)
    parser.add_argument('jmx_file', help='jmx file location',
                        type=str)
    return vars(parser.parse_args())


def update_test_case(duration, jmx_file, threads):
    root, ext = os.path.splitext(os.path.join(BASE_DIR, jmx_file))
    new_jmx_file = root + '_' + threads + '_' + str(int(time())) + ext
    new_jtl_file = root + '_' + threads + '_' + str(int(time())) + '.jtl'

    with open(jmx_file, 'r') as fr:
        with open(new_jmx_file, 'w+') as fw:
            content = fr.read()
            content = re.sub('loops">-?[0-9]+<', 'loops">-1<', content, 1)
            content = re.sub('num_threads">[0-9]+<',
                             'num_threads">{}<'.format(threads), content, 1)
            content = re.sub('scheduler">\w+<', 'scheduler">true<', content, 1)
            content = re.sub('duration">[0-9]*<',
                             'duration">{}<'.format(str(int(duration)*60)),
                             content, 1)

            fw.write(content)

    return new_jmx_file, new_jtl_file


def run_test_case(jmeter_path, new_jmx_file, new_jtl_file):
    cmd = '{jmeter_path} -n -t {new_jmx_file} -l {new_jtl_file}'.format(
        jmeter_path=jmeter_path,
        new_jmx_file=new_jmx_file,
        new_jtl_file=new_jtl_file)
    call(cmd.split())


def run(duration, jmx_file):
    jmeter_path, threads_list = get_conf(CONF_FILE)

    for threads in threads_list:
        new_jmx_file, new_jtl_file = update_test_case(duration, jmx_file, threads)
        run_test_case(jmeter_path, new_jmx_file, new_jtl_file)


if __name__ == '__main__':
    run(**get_args())
