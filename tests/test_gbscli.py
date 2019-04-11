import json
import tempfile

import pytest
from click.testing import CliRunner
from requests_mock import Mocker

import gbscli.entrypoint as cli
from gbscli import auth

CRED = {'account_id': 'AID', 'secret': 'SECRET'}


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def req_mock():
    with Mocker() as m:
        yield m


@pytest.fixture
def cred():
    with tempfile.NamedTemporaryFile() as f:
        f.write(json.dumps(CRED).encode('utf-8'))
        f.seek(0)
        yield f


URL = 'https://api.greedybandit.com'


def test_create_account(runner, req_mock):
    adapter = req_mock.post(URL + '/accounts', json={'A': 0})
    res = runner.invoke(cli.create_account, ['alan@mail.com', 'Alan'])

    assert adapter.called_once
    assert adapter.last_request.json() == {
        'email': 'alan@mail.com',
        'name': 'Alan',
    }
    assert res.exit_code == 0
    assert json.loads(res.output) == {'A': 0}


def test_req_svc_cred(runner, req_mock):
    adapter = req_mock.post(URL + '/accounts/service_credential_request?'
                                  'email=alan@mail.com')
    res = runner.invoke(cli.req_svc_cred, ['alan@mail.com'])

    assert adapter.called_once
    assert res.exit_code == 0
    assert json.loads(res.output) == {}


def test_describe_account(runner, req_mock, cred):
    adapter = req_mock.get(URL + '/accounts/AID', json={'A': 0},
                           request_headers=auth(CRED))
    res = runner.invoke(cli.describe_acount, ['--cred', cred.name])

    assert adapter.called_once
    assert res.exit_code == 0
    assert json.loads(res.output) == {'A': 0}


def test_list_services(runner, req_mock, cred):
    adapter = req_mock.get(URL + '/services', json={'A': 0},
                           request_headers=auth(CRED))
    res = runner.invoke(cli.list_services, ['--cred', cred.name])

    assert adapter.called_once
    assert res.exit_code == 0
    assert json.loads(res.output) == {'A': 0}


def test_get_service(runner, req_mock, cred):
    adapter = req_mock.get(URL + '/services/s0', json={'A': 0},
                           request_headers=auth(CRED))
    res = runner.invoke(cli.get_service, ['s0', '--cred', cred.name])

    assert adapter.called_once
    assert res.exit_code == 0
    assert json.loads(res.output) == {'A': 0}


def test_delete_service(runner, req_mock, cred):
    adapter = req_mock.delete(URL + '/services/s0', json={'A': 0},
                              request_headers=auth(CRED))
    res = runner.invoke(cli.delete_service, ['s0', '--cred', cred.name])

    assert adapter.called_once
    assert res.exit_code == 0
    assert json.loads(res.output) == {'A': 0}


def test_get_arms_stats(runner, req_mock, cred):
    header = auth(CRED)
    header.update({'Accept': 'text/csv'})
    adapter = req_mock.get(URL + '/stats/arms?svc_id=s&exp_id=e', json={},
                           request_headers=header)
    res = runner.invoke(cli.get_arm_stats, ['s', 'e', '--cred', cred.name])

    assert adapter.called_once
    assert res.exit_code == 0
    assert json.loads(res.output) == {}


def test_get_segs_stats(runner, req_mock, cred):
    header = auth(CRED)
    header.update({'Accept': 'text/csv'})
    adapter = req_mock.get(URL + '/stats/segs?svc_id=s&exp_id=e', json={},
                           request_headers=header)
    res = runner.invoke(cli.get_segs_stats, ['s', 'e', '--cred', cred.name])

    assert adapter.called_once
    assert res.exit_code == 0
    assert json.loads(res.output) == {}


def test_get_goals_stats(runner, req_mock, cred):
    header = auth(CRED)
    header.update({'Accept': 'text/csv'})
    adapter = req_mock.get(URL + '/stats/goals?svc_id=s&exp_id=e', json={},
                           request_headers=header)
    res = runner.invoke(cli.get_goals_stats, ['s', 'e', '--cred', cred.name])

    assert adapter.called_once
    assert res.exit_code == 0
    assert json.loads(res.output) == {}
