import click
import logging.config
import sys
import time


@click.command()
@click.option('--msg', type=str, default=None, required=True)
@click.option('--id', type=str, default='praetorian.')
@click.option('--level',
              type=click.Choice(['info', 'warning', 'error', 'critical']),
              default='info')
@click.option('--syslog-host', type=str, default='localhost')
@click.option('--syslog-port', type=int, default=6514)
@click.option('--syslog-cc-host', type=str, default='localhost')
@click.option('--syslog-cc-port', type=int, default=6515)
@click.option('--thales-host', type=str, default='10.22.22.12')
@click.option('--thales-port', type=int, default=514)
def main(msg, id, level, syslog_host, syslog_port, syslog_cc_host,
         syslog_cc_port, thales_host, thales_port):
    conf = {
        'version': 1,
        'formatters': {
            'default': {},
        },
        'handlers': {
            'syslog': {
                'class': 'hat.syslog.handler.SysLogHandler',
                'host': syslog_host,
                'port': syslog_port,
                'comm_type': 'TCP',
                'level': 'INFO',
                'formatter': 'default',
                'queue_size': 50,
            },
            'syslog_cc': {
                'class': 'hat.syslog.handler.SysLogHandler',
                'host': syslog_cc_host,
                'port': syslog_cc_port,
                'comm_type': 'TCP',
                'level': 'INFO',
                'formatter': 'default',
                'queue_size': 50,
            },
            'thales': {
                'class': 'hat.syslog.handler.SysLogHandler',
                'host': thales_host,
                'port': thales_port,
                'comm_type': 'UDP',
                'level': 'INFO',
                'formatter': 'default',
                'queue_size': 50,
            }
        },
        'root': {
                'level': 'INFO',
                'handlers': ['syslog', 'thales', 'syslog_cc']},
        'disable_existing_loggers': False}

    logging.config.dictConfig(conf)

    mlog = logging.getLogger(id)
    level = {'CRITICAL': 50,
             'ERROR': 40,
             'WARNING': 30,
             'INFO': 20,
             'DEBUG': 10,
             'NOTSET': 0}[level.upper()]
    mlog.log(level=level, msg=msg)
    time.sleep(0.1)


if __name__ == "__main__":
    sys.exit(main())
