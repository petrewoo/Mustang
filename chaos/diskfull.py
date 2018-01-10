#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
from string import Template
from subprocess import call

cmd_template = Template(
    'dd if=/dev/zero of=$dest/diskfull bs=1G count=$count iflag=fullblock')


def main(args):
    try:
        cmd = cmd_template.safe_substitute(args)
        call(cmd.split())
    except KeyboardInterrupt:
        print('Catch interrupt from keyboard, gracefully quit...')


def get_args():
    parser = argparse.ArgumentParser(
        "Genarate a diskfull file to fill full disk")
    parser.add_argument(
        '-d', dest='dest',
        help='Set where diskfull file you want to locate, default is /data',
        default='/data')
    parser.add_argument(
        '-c', dest='count',
        help='Set the size of diskfull file, default is 500G',
        type=int, default=500)
    return vars(parser.parse_args())


if __name__ == '__main__':
    main(**get_args())
