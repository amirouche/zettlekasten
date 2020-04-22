#!/usr/bin/env python
import json
import os
import shlex
import sys
import time
from datetime import datetime
from pathlib import Path
from subprocess import run
from tempfile import mkstemp


ROOT = Path(os.getcwd()).resolve()


VERSION = (0, 0, 2)


def now():
    return datetime.now().isoformat('T', 'seconds')


def init():
    with (ROOT / '.zk').open('w') as f:
        f.write(now())


def add():
    filename = now() + '.json'
    with (ROOT / filename).open('w') as f:
        fd, filepath = mkstemp()
        os.close(fd)

        editor = os.environ.get('EDITOR', 'vi')
        os.system('{} "{}"'.format(editor, filepath))

        with open(filepath) as fi:
            body = fi.read()

        obj = {
            'timestamp': now(),
            'body': body,
            'links': [],
        }

        f.write(json.dumps(obj))


def dolink(a, b):
    with open(a, 'r') as f:
        content = f.read()
    content = json.loads(content)
    content['links'].append(b)
    with open(a, 'w') as f:
        f.write(json.dumps(content))

def link(a, b):
    dolink(a, b)
    dolink(b, a)


COMMAND_TO_FUNCTION = {
    'init': init,
    'add': add,
    'link': link,
}


def main():
    try:
        command = sys.argv[1]
    except IndexError:
        print("No command found!")
        sys.exit(1)

    arguments = sys.argv[2:]

    try:
        function = COMMAND_TO_FUNCTION[command]
    except KeyError:
        print('Command unknown!')
        sys.exit(1)

    sys.exit(function(*arguments))


if __name__ == '__main__':
    main()
