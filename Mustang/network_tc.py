#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from subprocess import call
import time
import argparse
import yaml
import os

clean_cmd = 'sudo tc qdisc del dev eth0 root'


def task(mode, cmd_list):
    try:
        while 1:
            for cmd in cmd_list:
                call(cmd.split())
                if mode == 2:
                    if cmd == cmd_list[0]:
                        tmp = 'ON'
                    else:
                        tmp = 'OFF'
                    result = raw_input(
                        'Tc rule {: >4}.Plz press Enter to continue...'.format(tmp))
                    # exit program graceful if any input
                    if result:
                        return
                else:
                    time.sleep(10)
    except KeyboardInterrupt:
        print('Catch interrupt signal, shutdown script graceful...')
    finally:
        call(cmd_list[1].split())


def get_arg():
    args_list = []
    parse = argparse.ArgumentParser()
    parse.add_argument(
        '-m', '--mode',
        help='Set script excute mode 1:automatic, 2:manual, \
        default is automatic',
        type=int, default=1)
    parse.add_argument(
        '-c', '--config',
        help='Set where config file read from tcConfig.yaml',
        type=str,
        default='tcConfig.yaml')
    args = parse.parse_args()
    args_list.append(args.mode)
    args_list.append(args.config)
    return args_list


def load_config(path, file):
    try:
        with open(path + '/' + file, 'r') as f:
            return yaml.load(f)
    except IOError:
        print('Open {} failed, Plz check the config file\n'.format(file))
        exit(1)


def _cmd_list_constructor(path, file):
    cmd_list = []
    cmd_list.append(load_config(path, file))
    cmd_list.append(clean_cmd)
    return cmd_list


def main(mode, config_file):
    path = os.path.dirname(__file__)
    cmd_list = _cmd_list_constructor(path, config_file)
    task(mode, cmd_list)


if __name__ == '__main__':
    args = get_arg()
    main(*args)
