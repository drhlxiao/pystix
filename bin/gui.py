#!/usr/bin/python3
import sys
import os
sys.path.append('.')
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from stix.ui import main
def start():
    main.main()
if __name__ == '__main__':
    start()

