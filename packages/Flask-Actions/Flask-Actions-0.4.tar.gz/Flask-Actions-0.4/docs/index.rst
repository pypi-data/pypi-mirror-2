Welcome to Flask-Actions's documentation!
=========================================
The **Flask-Actions** extension provides support for writing external actions in Flask. This includes running a development server, a customized Python shell,a fastcgi server like django . 

**Flask-Actions** uses werkzeug management script utilities,you'd rather dive into it's documentation :

-  `Werkzeug Documentation - Management Script Utilities <http://werkzeug.pocoo.org/documentation/dev/script.html/>`_

A normal startup scripts is like this:

    # manage.py

    from flaskdagger import app

    from flaskext.actions import Manager

    manager = Manager(app)

    if __name__ == "__main__":
        manager.run()

And you can run 'python manage.py --help' to see more ::


    usage: manage.py <action> [<options>]
           manage.py --help

    actions:
      bshell:
        run shell use bpython
                

      runfcgi:
        run application use flup
        you can choose these arguments:
        protocol :   scgi, fcgi or ajp
        method   :   threaded or fork
        children :   number of threads or processes

        -h, --hostname                string    
        -p, --port                    integer   3001
        --protocol                    string    scgi
        --method                      string    threaded
        --children                    integer   20
        --daemonize
        --pidfile                     string    /var/run/flask.pid
        --workdir                     string    .
        --outlog                      string    /dev/null
        --errlog                      string    /dev/null
        --umask                       integer   18

      runtwisted:
        run application use twisted http server
        @reactor_type: [default 1]
            1       epoll   reactor
            2       poll    reactor
            3       kqueue  reactor
            4       iocp    reactor
            other   select  reactor

        -p, --port                    integer   8000
        -r, --reactor-type            integer   1


      runserver:
        Start a new development server.

        -h, --hostname                string    0.0.0.0
        -p, --port                    integer   7777
        --no-reloader
        --no-debugger
        --no-evalex
        --no-threaded
        --processes                   integer   1

      shell:
        Start a new interactive python session.

        --no-ipython

Deploy use fastcgi
------------------------
To start your server,run the `runfcgi` command::

    ./manage.py runfcgi [options]

Select your preferred protocol by using the ``protocol=<protocol_name>`` option
with ``./manage.py runfcgi`` -- where ``<protocol_name>`` may be one of: ``scgi`` (the default),
``fcgi`` or ``ajp``. 

Running a threaded server on a TCP port::

    ./manage.py runfcgi method=threaded host=127.0.0.1 port=3033

Running a preforked server on a Unix domain socket::

    ./manage.py runfcgi method=prefork socket=/home/user/mysite.sock pidfile=flask.pid

Run without daemonizing (backgrounding) the process (good for debugging)::

    ./manage.py runfcgi daemonize=false socket=/tmp/mysite.sock maxrequests=1

Stopping the FastCGI daemon
`````````````````````````````

If you have the process running in the foreground, it's easy enough to stop it:
Simply hitting ``Ctrl-C`` will stop and quit the FastCGI server. However, when
you're dealing with background processes, you'll need to resort to the Unix
``kill`` command.

If you specify the ``pidfile`` option to `runfcgi`, you can kill the
running FastCGI daemon like this::

    kill `cat $PIDFILE`

...where ``$PIDFILE`` is the ``pidfile`` you specified.

Setup Nginx
``````````````````````````````
Run the application using fastcgi daemonize mode ,like this::

    python manage.py runfcgi --protocol=fcgi -p 7777  --daemonize --pidfile=/var/run/flaskapp.pid

but you would rather use an init.d scripts to execute above commands ,
then you can configure the nginx like this ::

      upstream flaskapp {
         server 127.0.0.1:7777;
         }

      server {
      listen 8080;
      server_name  127.0.0.0;


      location / {
        fastcgi_pass  flaskapp;
        fastcgi_param REQUEST_METHOD    $request_method;
        fastcgi_param QUERY_STRING      $query_string;
        fastcgi_param CONTENT_TYPE      $content_type;
        fastcgi_param CONTENT_LENGTH    $content_length;
        fastcgi_param SERVER_ADDR       $server_addr;
        fastcgi_param SERVER_PORT       $server_port;
        fastcgi_param SERVER_NAME       $server_name;
        fastcgi_param SERVER_PROTOCOL   $server_protocol;
        fastcgi_param PATH_INFO         $fastcgi_script_name;
        fastcgi_param REMOTE_ADDR       $remote_addr;
        fastcgi_param REMOTE_PORT       $remote_port;
        fastcgi_pass_header Authorization;
        fastcgi_intercept_errors off;
      }
