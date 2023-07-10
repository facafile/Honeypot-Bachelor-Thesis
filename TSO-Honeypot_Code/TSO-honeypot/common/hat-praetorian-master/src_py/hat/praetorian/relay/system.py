from pathlib import Path
import click
import sys
import logging

from hat import json
import hat.orchestrator.main


mlog: logging.Logger = logging.getLogger(__name__)

default_conf_path = Path('relay.yaml')
default_gen_path = Path('gen/relay/')


log_conf = {
    'version': 1,
    'formatters': {'default': {}},
    'handlers': {
        'syslog': {
            'class': 'hat.syslog.handler.SysLogHandler',
            'host': '127.0.0.1',
            'port': 6514,
            'comm_type': 'TCP',
            'level': 'INFO',
            'formatter': 'default',
            'queue_size': 50}},
    'root': {
        'level': 'INFO',
        'handlers': ['syslog']},
    'disable_existing_loggers': False}


@click.command()
@click.option('--conf-path', type=Path,
              default=default_conf_path)
@click.option('--gen-path', type=Path,
              default=default_gen_path)
def main(conf_path, gen_path):
    _write_component_confs(conf_path, gen_path)
    orchestrator_conf_path = _orchestrator_conf_path(gen_path)
    hat.orchestrator.main.main(['--conf', str(orchestrator_conf_path)])


def _write_component_confs(conf_path, gen_path):
    gen_path.mkdir(parents=True, exist_ok=True)
    relay_conf_path = gen_path / 'relay.yaml'
    syslog_conf_path = gen_path / 'syslog.yaml'
    orchestrator_conf_path = _orchestrator_conf_path(gen_path)

    relay_conf = json.decode_file(conf_path)
    relay_conf = json.set_(relay_conf, ['log'], log_conf)
    json.encode_file(relay_conf, relay_conf_path)

    orchestrator_conf = {
        'type': 'orchestrator',
        'log': log_conf,
        'components': [
            {'name': 'syslog',
             'args': [sys.executable, '-m', 'hat.syslog.server',
                      '--conf', str(syslog_conf_path)],
             'delay': 0,
             'revive': False,
             'start_delay': 0.5,
             'create_timeout': 2,
             'sigint_timeout': 5,
             'sigkill_timeout': 2},
            {'name': 'relay',
             'args': [sys.executable, '-m', 'hat.praetorian.relay',
                      '--conf-path', str(relay_conf_path)],
             'delay': 0,
             'revive': False,
             'start_delay': 2,
             'create_timeout': 2,
             'sigint_timeout': 5,
             'sigkill_timeout': 2},
             ],
        'ui': {'address': 'http://0.0.0.0:23021'}}
    json.encode_file(orchestrator_conf, orchestrator_conf_path)

    syslog_conf = {
        'db_disable_journal': False,
        'db_enable_archive': True,
        'db_high_size': 1000000,
        'db_low_size': 1000,
        'db_path': str(gen_path / 'syslog.db'),
        'log': {'version': 1},
        'syslog_addr': 'tcp://127.0.0.1:6514',
        'type': 'syslog',
        'ui_addr': 'http://0.0.0.0:23020'}
    json.encode_file(syslog_conf, syslog_conf_path)


def _orchestrator_conf_path(gen_path):
    return gen_path / 'orchestrator.yaml'


if __name__ == '__main__':
    sys.exit(main())
