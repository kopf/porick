#!/bin/bash
# Start porick a little less painfully
#
# Stephen Shaw <stesh@netsoc.tcd.ie>


# Change these settings as necessary to fit your installation
APPDIR='/srv/subdomains/porick'
APPCONFIG="$APPDIR/production.ini"

PIDFILE="$APPDIR/porick.pid"

PYTHONPATH=':/usr/local/lib/python2.6/dist-packages/FormEncode-1.2.4-py2.6.egg:/usr/local/lib/python2.6/dist-packages/simplejson-2.5.2-py2.6.egg:/usr/local/lib/python2.6/dist-packages/decorator-3.3.3-py2.6.egg:/usr/local/lib/python2.6/dist-packages/nose-1.1.2-py2.6.egg:/usr/local/lib/python2.6/dist-packages/Mako-0.7.0-py2.6.egg:/usr/local/lib/python2.6/dist-packages/WebError-0.10.3-py2.6.egg:/usr/local/lib/python2.6/dist-packages/WebTest-1.3.4-py2.6.egg:/usr/local/lib/python2.6/dist-packages/Tempita-0.5.1-py2.6.egg:/usr/local/lib/python2.6/dist-packages/SQLAlchemy-0.7.7-py2.6-linux-x86_64.egg:/usr/local/lib/python2.6/dist-packages/Pylons-1.0.1rc1-py2.6.egg:/usr/local/lib/python2.6/dist-packages/WebOb-1.2b3-py2.6.egg:/usr/local/lib/python2.6/dist-packages/MarkupSafe-0.15-py2.6.egg:'

running () {
    [ -f $PIDFILE ]
}

die () {
    echo "$1" >/dev/stderr
    exit 1
}

pid () {
    cat $PIDFILE | head -n 1
}

start_server () {
    if running; then 
        die "Porick is already running (PID: $(pid))"
    fi

    cd $APPDIR
    exec su -m www-data -c "PYTHONPATH='$PYTHONPATH' paster serve $APPCONFIG --pid-file=$PIDFILE &"
}
stop_server () {
    if ! running; then
        die "Porick isn't running"
    fi

    kill $(pid) && rm -f $PIDFILE
}

server_status () {
    if running; then 
        echo "Running (PID: $(pid))"
    else
        echo "Not running"
    fi
}

[ "$1" = "start" ] && (shift; start_server; exit)
[ "$1" = "stop" ] && (shift; stop_server; exit)
[ "$1" = "status" ] && (shift; server_status; exit)


cat <<EOF 
Usage: $0 <start|stop|status>
EOF
