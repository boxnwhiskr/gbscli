import json

import click
import requests

from gbscli import add_options, CLIError, render_res, get_cred, render_error, \
    auth

common_options = [
    click.option('--cred', help='Absolute path to the credential file'),
    click.option('--url', default='https://api.greedybandit.com',
                 help='GreedyBandit service URL')
]


@click.group()
def cli():
    """GreedyBandit is a cloud-based A/B testing and optimization engine.

    More information is available on https://api.greedybandit.com
    """
    pass


@cli.group()
def account():
    """Manage account."""
    pass


@account.command(name='create')
@click.argument('email')
@click.argument('name')
@add_options(common_options)
def create_account(email, name, cred, url):
    """Create new account.

    Create new account with given EMAIL and NAME. An email containing a link
    to a service credential will be sent."""
    try:
        req = url + '/accounts'
        res = requests.post(req, json={
            'email': email,
            'name': name,
        })
        render_res(res)
    except CLIError as e:
        render_error(e.asdict())


@account.command(name='credential')
@click.argument('email')
@add_options(common_options)
def req_svc_cred(email, cred, url):
    """Request new service credential.

    Let the service send an e-mail containing a link to new service credential.
    Calling this API alone won't affect the current credential."""
    try:
        req = url + '/accounts/service_credential_request?email=' + email
        res = requests.post(req)
        render_res(res)
    except CLIError as e:
        render_error(e.asdict())


@account.command(name='describe')
@add_options(common_options)
def describe_acount(cred, url):
    """Get account information."""
    try:
        credential = get_cred(cred)
        headers = auth(credential)
        req = url + '/accounts/' + credential['account_id']
        res = requests.get(req, headers=headers)
        render_res(res)
    except CLIError as e:
        render_error(e.asdict())


@cli.group()
def service():
    """Manage services."""
    pass


@service.command(name='list')
@add_options(common_options)
def list_services(cred, url):
    """Get all service configurations"""
    try:
        headers = auth(get_cred(cred))
        req = url + '/services'
        res = requests.get(req, headers=headers)
        render_res(res)
    except CLIError as e:
        render_error(e.asdict())


@service.command(name='describe')
@click.argument('svc_id')
@add_options(common_options)
def get_service(svc_id, cred, url):
    """Get service configuration"""
    try:
        headers = auth(get_cred(cred))
        req = url + '/services/' + svc_id
        res = requests.get(req, headers=headers)
        render_res(res)
    except CLIError as e:
        render_error(e.asdict())


@service.command(name='delete')
@click.argument('svc_id')
@add_options(common_options)
def delete_service(svc_id, cred, url):
    """Delete service configuration"""
    try:
        headers = auth(get_cred(cred))
        req = url + '/services/' + svc_id
        res = requests.delete(req, headers=headers)
        render_res(res)
    except CLIError as e:
        render_error(e.asdict())


@service.command(name='edit')
@click.argument('svc_id')
@add_options(common_options)
def edit_service(svc_id, cred, url):
    """Create or update service configuration"""
    try:
        headers = auth(get_cred(cred))

        # Get current config
        req = url + '/services/' + svc_id
        res = requests.get(req, headers=headers)
        if res.status_code == 200:
            cur = res.json()
            read_only_fields = ['account_id', 'svc_id', 'update_dt']
            for f in read_only_fields:
                del cur[f]
        elif res.status_code == 404:
            cur = {
                'experiments': [],
                'goals': [],
            }
        else:
            render_res(res)
            return

        # Launch editor
        new = click.edit(json.dumps(cur, indent=4), require_save=True,
                         extension='.json')

        # Do nothing if user didn't save the content on the editor
        if new is None:
            click.secho('Configuration not saved.', fg='yellow')
            return

        try:
            parsed = json.loads(new)
        except ValueError as e:
            # Catch ValueError since python 3.4 doesn't have JSONDecodeError
            raise CLIError(str(e))
        else:
            res = requests.put(req, headers=headers, json=parsed)
            render_res(res)
    except CLIError as e:
        render_error(e.asdict())


@cli.group()
def stats():
    """Get statistics."""
    pass


@stats.command(name='arms')
@click.argument('svc_id')
@click.argument('exp_id')
@add_options(common_options)
def get_arm_stats(svc_id, exp_id, cred, url):
    try:
        req = url + '/stats/arms?svc_id=' + svc_id + '&exp_id=' + exp_id
        header = auth(get_cred(cred))
        header.update({'Accept': 'text/csv'})
        res = requests.get(req, headers=header)
        click.echo(res.text)
    except CLIError as e:
        render_error(e.asdict())


@stats.command(name='seg')
@click.argument('svc_id')
@click.argument('exp_id')
@add_options(common_options)
def get_segs_stats(svc_id, exp_id, cred, url):
    try:
        req = url + '/stats/segs?svc_id=' + svc_id + '&exp_id=' + exp_id
        header = auth(get_cred(cred))
        header.update({'Accept': 'text/csv'})
        res = requests.get(req, headers=header)
        click.echo(res.text)
    except CLIError as e:
        render_error(e.asdict())


@stats.command(name='goal')
@click.argument('svc_id')
@click.argument('exp_id')
@add_options(common_options)
def get_goals_stats(svc_id, exp_id, cred, url):
    try:
        req = url + '/stats/goals?svc_id=' + svc_id + '&exp_id=' + exp_id
        header = auth(get_cred(cred))
        header.update({'Accept': 'text/csv'})
        res = requests.get(req, headers=header)
        click.echo(res.text)
    except CLIError as e:
        render_error(e.asdict())
