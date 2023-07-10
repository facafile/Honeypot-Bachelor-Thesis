Hat PRAETORIAN - linux distribution package
===========================================

Prerequisits
------------

* 64bit Linux
* Python 3.8


Installation
------------

In the remainder of this text, one refers to `relay` application of the
Hat PRAETORIAN. Explanation corresponds directly to `commander` application. 


As ``root`` run install_relay.sh::

    $ sudo ./install_relay.sh


If previous installation to same destination folder is detected, previous
installation is uninstalled prior to new installation execution. During
uninstallation of previous distribution, data folder (default
`/var/opt/hat-praetorian`) is not removed - configuration and databses are not
removed.

Default installation paths:

    * /opt/hat-praetorian

        application installation path

    * /var/opt/hat-praetorian

        configuration and data path

    * /usr/bin

        executables symlink paths

    * /usr/share/applications

        desktop file paths

    * /usr/share/pixmaps

        icon paths

    * /etc/systemd/system

        systemd service paths


Uninstall
---------

Installation folder (default `/opt/hat-praetorian`) contains ``uninstall.sh`` which
can be used for removing previous installation::

    $ sudo /opt/hat-praetorian/uninstall.sh

Uninstall procedure doesn't remove content of data folder (default
`/var/opt/hat-praetorian`).


Running
-------

This package contains multiple services that can be run independently:

* relay


Running relay
^^^^^^^^^^^^^

Installation procedure registers `hat-praetorian-relay` systemd service.

Starting system service::

    $ sudo systemctl start hat-praetorian-relay

Stopping system service::

    $ sudo systemctl stop hat-praetorian-relay

Enable automatic service run after boot::

    $ sudo systemctl enable hat-praetorian-relay

Disable automatic service run after boot::

    $ sudo systemctl disable hat-praetorian-relay

Current status of service::

    $ sudo systemctl status hat-praetorian-relay

Service journal navigation (log of console output):

    $ sudo journalctl -u hat-praetorian-relay

Additionally, system can be run with `hat-praetorian-relay` command. It is assumed
that current working directory is data directory - it should contain
appropriate ``relay.yaml`` configuration.
