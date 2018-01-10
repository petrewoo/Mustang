#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from subprocess import call
import time
import argparse

cmdlist = ('sudo iptables -A INPUT -p tcp -m tcp --dport 5672 -j DROP',
           'sudo iptables -F')


def main(mode):
    try:
        while 1:
            for cmd in cmdlist:
                call(cmd.split())
                if mode == 2:
                    if cmd == cmdlist[0]:
                        tmp = 'ON'
                    else:
                        tmp = 'OFF'
                    result = raw_input('Rule {: >4}.Plz press Enter to continue...'.format(tmp))
                    # exit program graceful
                    if result:
                        return
                else:
                    time.sleep(10)
    except KeyboardInterrupt:
        print('Catch interrupt signal, shutdown script graceful...')
    finally:
        call(cmdlist[1].split())


def get_arg():
    parse = argparse.ArgumentParser()
    parse.add_argument('-m', '--mode', help='Set script excute mode 1:automatic, 2:manual, default is automatic', type=int, default=1)
    args = parse.parse_args()
    return args.mode


if __name__ == '__main__':
    main(get_arg())
