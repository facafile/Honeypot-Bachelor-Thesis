Praetorian command attack
=========================

This script is aimed to send a iec104 Double command to a remote slave. It first
connects to the remote slave with specific `host` and `port` and sends a double
command with `asdu`, `io` and `value`. Upon command is sent, one waits for the
command response. Upon receiving the response, connection is closed and script
ends.

Script is called with `./command_attack.sh`:

    $ ./command_attack.sh --help

Usage: command_attack.py [OPTIONS]

Options:
  --host TEXT       [required]
  --port INTEGER    [required]
  --asdu INTEGER    [required]
  --io INTEGER      [required]
  --value [OFF|ON]  [required]
  --help            Show this message and exit.

where:
    `host` is remote iec104 slave host.

    `port` is remote iec104 slave port.

    `asdu` is command asdu address.

    `io` is command io address.

    `value` is command value ``ON``, or ``OFF``.

example

    $ ./command_attack.sh --host 127.0.0.1 --port 2404 --asdu 1 --io 2 --value OFF

