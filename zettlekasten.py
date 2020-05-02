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

from jinja2 import Environment
from jinja2 import FileSystemLoader

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

ROOT = Path(os.getcwd()).resolve()


VERSION = (0, 0, 2)


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            out = '\n<div><pre>{}</pre></div>\n'
            return out.format(mistune.escape(code.strip()))
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)


def jinja(template, templates, **context):
    templates = os.path.abspath(templates)
    env = Environment(loader=FileSystemLoader((templates,)))
    template = env.get_template(template)
    out = template.render(markdown=markdown, **context)
    return out

def now():
    return datetime.now().isoformat('T', 'seconds')


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
        note = f.read()
    note = json.loads(note)
    basename = b.split('.')[0]
    note['links'].append(basename)
    with open(a, 'w') as f:
        f.write(json.dumps(note))

def link(a, b):
    dolink(a, b)
    dolink(b, a)


def render_one(filepath):
    with filepath.open() as f:
        note = json.load(f)
    basename = filepath.name.split('.')[0]
    html = jinja('note.jinja2', str(ROOT), title="hyper.dev", note=note)
    filepath = (filepath.parent / (basename + '.html'))
    with filepath.open('w') as f:
        f.write(html)
    return basename

def render():
    notes = [render_one(f) for f in ROOT.glob('*.json')]
    notes = sorted(notes)
    html = jinja('index.jinja2', str(ROOT), title="hyper.dev", notes=notes)
    with (ROOT / 'index.html').open('w') as f:
        f.write(html)



COMMAND_TO_FUNCTION = {
    'add': add,
    'link': link,
    'render': render,
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
