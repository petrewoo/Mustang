#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import multiprocessing as mp
import os
import signal
import time

from subprocess import Popen


class InterruptLoop(Exception):
    """Interrupt internal loop"""


def task(interval):

    def handler(signum, frame):
        """Use KeyboardInterrupt as singal from outside"""
        raise KeyboardInterrupt

    def alarm_handler(signum, frame):
        raise InterruptLoop

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGALRM, alarm_handler)

    p_name = mp.current_process().name
    with open(os.devnull, 'w') as devnull:
        try:
            while 1:
                p = Popen('openssl speed'.split(),
                          stdout=devnull, stderr=devnull,
                          preexec_fn=os.setsid)
                signal.alarm(interval)
                try:
                    p.wait()
                except KeyboardInterrupt:
                    raise
                except InterruptLoop:
                    try:
                        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                        time.sleep(interval)
                    except KeyboardInterrupt:
                        raise
                    except Exception, e:
                        print('{}: {}'.format(p_name, e))
        except KeyboardInterrupt:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            except (OSError, InterruptLoop):
                pass
            except Exception, e:
                print('{}: {}'.format(p_name, e))


def main(minute, interval):
    p_list = []
    duration = minute * 60
    delay = 0.005

    for _ in range(mp.cpu_count()):
        p = mp.Process(target=task, args=(interval,))
        p_list.append(p)

    base_time = time.time()

    for p in p_list:
        p.start()

    try:
        if duration != 0:
            while (time.time() - base_time < duration):
                time.sleep(delay)
        else:
            while 1:
                time.sleep(delay)

        print('Time over {}s, Quit!'.format(duration))
    except KeyboardInterrupt:
        print('Interrupt from keyboard, Quit gracefully!')
    finally:
        for p in p_list:
            p.terminate()
            p.join()


def get_args():
    parser = argparse.ArgumentParser('Cpu burn maker')
    parser.add_argument(
        '-d', dest='duration',
        help='Set duration(minute) which greater than or equal to zero, \
              default value is zero which means infinity loop',
        type=float,
        default=0)
    parser.add_argument(
        '-i', dest='interval',
        help='Set interval(second) which greater than or equal to zero, \
              default value is zero which means no interval',
        type=int,
        default=0)
    return vars(parser.parse_args())


if __name__ == '__main__':
    main(**get_args())
