Praetorian logging script
=========================

This script logs arbitrary messages to hat-syslog server and to another
syslog server called 'thales' over UDP.

Script is called with `./praet_logger.sh`:

    $ ./praet_logger.sh --help

Usage: praet_logger.py [OPTIONS]

Options:
  --msg TEXT                      [required]
  --id TEXT
  --level [info|warning|error|critical]
  --syslog-host TEXT
  --syslog-port INTEGER
  --thales-host TEXT
  --thales-port INTEGER
  --help

where:
    `msg` is arbitrary message that wants to be sent. This is the only required
          argument.

    `id` is message ID, that is a dot-separated hierarchical name like `a.b.c`.
         Defaults to `praetorian.`

    `level` is logging level, can be one of: info, warning, error, critical.
            defaults to `info`.

    `syslog-host` is host of the hat-syslog server. Defaults to 'localhost'.

    `syslog-port` is port of the hat-syslog server. Defaults to 6514.

    `thales-host` is host of the thales server. Defaults to '10.22.22.12'.

    `thales-port` is port of the thales server. Defaults to 514.

Examples
--------

* Example 1 - logs message 'blabla' to level `info`, with id `praetorian.`
    
    $ ./praet_logger.sh --msg=blabla

* Example 2 - logs message 'juhuu' to level `warning`, with id `a.b.c`

    $ ./praet_logger.sh --msg=juhuu --id=a.b.c --level=warning 


