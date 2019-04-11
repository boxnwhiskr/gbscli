import base64
import json
import os
from os.path import expanduser

import click

# Use os.path.expanduser() since Python 3.4 doesn't have pathlib.Path()
DEFAULT_CRED_PATH = os.path.join(expanduser('~'), '.config', 'gbs',
                                 'credential.json')


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def get_cred(path):
    path = path or DEFAULT_CRED_PATH
    if not os.path.isfile(path):
        raise CLIError(
            'Credential not found: ' + path,
            detail='Save your credential to "%s". You may also specify a '
                   'custom location using --cred option.' % DEFAULT_CRED_PATH,
        )
    with open(path, 'r') as f:
        return json.load(f)


def auth(cred):
    token = cred['account_id'] + ':' + cred['secret']
    basic_auth = base64.b64encode(token.encode("utf-8")).decode("utf-8")
    return {'Authorization': 'Basic ' + basic_auth}


def render_res(res):
    body = json.loads(res.content.decode('utf-8') or '{}')

    if res.status_code < 400:
        click.echo(json.dumps(body, indent=4))
    else:
        render_error(body)


def render_error(err):
    width, _ = click.get_terminal_size()
    click.secho('[Error] %s' % err['title'], fg='red')

    if err.get('detail', ''):
        click.secho(click.wrap_text(err['detail'], width=width))
    else:
        click.echo(json.dumps(err, indent=4))


class CLIError(Exception):
    def __init__(self, title, detail=None):
        self.title = title
        self.detail = detail

    def asdict(self):
        return {
            'title': self.title,
            'detail': self.detail,
        }
