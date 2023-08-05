============
SimpleDaemon
============

A fork of `Shane Hathaway's daemon.py <http://hathawaymix.org/Software/Sketches/daemon.py>`_ script.

Features
========

* reads the command line
* reads a configuration file
* configures logging
* calls root-level setup code
* drops privileges
* calls user-level setup code
* detaches from the controlling terminal
* checks and writes a pidfile


Example
=======
Writing a daemon requires creating two files, a daemon
file and a configuration file with the same name.

hellodaemon.py::

    import simpledaemon
    import logging
    import time

    class HelloDaemon(simpledaemon.Daemon):
        default_conf = '/etc/hellodaemon.conf'
        section = 'hello'

        def run(self):
            while True:
                logging.info('The daemon says hello')
                time.sleep(1)

    if __name__ == '__main__':
        HelloDaemon().main()

hellodaemon.conf::

    [hello]
    uid =
    gid =
    pidfile = ./hellodaemon.pid
    logfile = ./hellodaemon.log
    loglevel = info
