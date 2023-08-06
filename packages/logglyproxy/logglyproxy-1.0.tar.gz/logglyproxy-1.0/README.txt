logglyproxy
===========

This is a syslog server proxy.
The messages it receives are forwarded to Loggly__ via HTTPS.
The server uses gevent and keep-alive http sessions for performance.

__ http://www.loggly.com

Usage:

::

    logglyproxy -c config_file

Here's an example config file:

::

    [logglyproxy]
    bind_address = 127.0.0.1
    port = 5140
    apikey = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

And an LSB init script:

::

    #! /bin/sh
    ### BEGIN INIT INFO
    # Provides:          logglyproxy
    # Required-Start:    $local_fs $remote_fs $network $syslog
    # Required-Stop:     $local_fs $remote_fs $network $syslog
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # X-Interactive:     false
    # Short-Description: Start/stop logglyproxy

    DAEMON="logglyproxy"
    DAEMON_USR=logglyproxy
    DAEMON_GRP=logglyproxy
    INSTALLPATH=/path/to/logglyproxy/virtualenv
    PIDFILE=/var/run/logglyproxy.pid

    . /lib/lsb/init-functions

    case "$1" in
      start)
        log_begin_msg "Starting logglyproxy server..."

        # Activate the virtual environment
        . $INSTALLPATH/bin/activate

        start-stop-daemon --background --make-pidfile \
            --start --pidfile $PIDFILE \
            --user $DAEMON_USR --group $DAEMIN_GRP \
            --chuid $DAEMON_USR \
            --exec "$INSTALLPATH/bin/$DAEMON"  -- -c /etc/logglyproxy.cfg
        log_end_msg $?
        ;;
      stop)
        log_begin_msg "Stopping logglyproxy server..."
        start-stop-daemon --stop --pidfile $PIDFILE --verbose
        log_end_msg $?
        ;;
      *)
        log_success_msg "Usage: /etc/init.d/logglyproxy {start|stop}"
        exit 1
        ;;
    esac

    exit 0


