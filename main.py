#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import ConfigParser
from runner.runner import Runner


def run(conf):
    cf = ConfigParser.ConfigParser()
    cf.read(conf)
    runner = Runner(cf)
    runner.run()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hf:', ['configfile='])
    except getopt.GetoptError:
        print 'main.py -f <configfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -f <configfile>'
            sys.exit()
        elif opt in ('-f', '--configfile'):
            run(arg)
        else:
            print 'unknown args', opt
            sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])

