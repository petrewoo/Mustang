#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
from string import Template
from subprocess import call

cmd_template = Template(
    'dd if=/dev/zero of=$dest/ioburn bs=1G count=10 iflag=fullblock')


def main(args):
    try:
        while 1:
            cmd = cmd_template.safe_substitute(args)
            call(cmd.split())
    except KeyboardInterrupt:
        print('Catch interrupt from keyboard, gracefully quit...')


def get_args():
    parser = argparse.ArgumentParser(
        "Genarate a ioburn file to burn I/O")
    parser.add_argument(
        '-d', dest='dest',
        help='Set where ioburn file you want to locate, default is /data',
        default='/data')
    args = parser.parse_args()

    args_dict = {}
    args_dict['dest'] = args.dest
    return args_dict


if __name__ == '__main__':
    main(get_args())
