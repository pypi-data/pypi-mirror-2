# -*- coding: utf-8 -
#
# This file is part of grainbows released under the MIT license. 
# See the NOTICE for more information.

import optparse as op
import os
import pkg_resources
import sys

from grainbows import __version__

from gunicorn.main import options, configure_logging, daemonize
from gunicorn import util
from grainbows.config import Config

_proctitle = None
def patch_proctitle():
    global _proctitle
    if _proctitle: 
        return
    try:
        from setproctitle import setproctitle
        def grainbows_setproctitle(title):
            setproctitle("grainbows: %s" % title)
            
        util._setproctitle = grainbows_setproctitle
    except ImportError:
        pass
    _proctitle = True

patch_proctitle()

def grainbows_options():
    goptions = [
        op.make_option('--use', dest='use', action="store",
            help='method to use (eventlet, gevent)')
    ]
    
    goptions.extend(options())
    return goptions

        
def main(usage, get_app):
    """ function used by different runners to setup options 
    ans launch the arbiter. """
    
    
    
    parser = op.OptionParser(usage=usage, option_list=grainbows_options(),
                    version="%prog " + __version__)
    opts, args = parser.parse_args()
    
    app = get_app(parser, opts, args)
    conf = Config(opts.__dict__, opts.config)
    
    arbiter = conf.arbiter(conf.address, conf.workers, app, config=conf, 
                debug=conf['debug'], pidfile=conf['pidfile'])
    if conf['daemon']:
        daemonize()
    else:
        os.setpgrp()
    configure_logging(conf)
    arbiter.run()
    
def paste_server(app, global_conf=None, host="127.0.0.1", port=None, 
            *args, **kwargs):
    """ Paster server entrypoint to add to your paster ini file:
    
        [server:main]
        use = egg:gunicorn#main
        host = 127.0.0.1
        port = 5000
    
    """
    options = kwargs.copy()
    if port and not host.startswith("unix:"):
        bind = "%s:%s" % (host, port)
    else:
        bind = host
    options['bind'] = bind

    if global_conf:
        for key, value in list(global_conf.items()):
            if value and value is not None:
                if key == "debug":
                    value = (value == "true")
                options[key] = value
        options['default_proc_name'] = options['__file__']
           
    conf = Config(options)
    arbiter = conf.arbiter(conf.address, conf.workers, app, debug=conf["debug"], 
                    pidfile=conf["pidfile"], config=conf)
    if conf["daemon"] :
        daemonize()
    else:
        os.setpgrp()
    configure_logging(conf)
    arbiter.run()
    
def run():
    """ main runner used for gunicorn command to launch generic wsgi application """
    
    sys.path.insert(0, os.getcwd())
    
    def get_app(parser, opts, args):
        if len(args) != 1:
            parser.error("No application module specified.")


        opts.default_proc_name = args[0]
            
        try:
            return util.import_app(args[0])
        except:
            parser.error("Failed to import application module.")

    main("%prog [OPTIONS] APP_MODULE", get_app)
    
def run_django():
    """ django runner for gunicorn_django command used to launch django applications """
    
    def settings_notfound(path):
        error = "Settings file '%s' not found in current folder.\n" % path
        sys.stderr.write(error)
        sys.stderr.flush()
        sys.exit(1)

    def get_app(parser, opts, args):
        import django.core.handlers.wsgi

        project_path = os.getcwd()
        
        if args:
            settings_path = os.path.abspath(os.path.normpath(args[0]))
            if not os.path.exists(settings_path):
                settings_notfound(settings_path)
            else:
                project_path = os.path.dirname(settings_path)
        else:
             settings_path = os.path.join(project_path, "settings.py")
             if not os.path.exists(settings_path):
                 settings_notfound(settings_path)
        
        project_name = os.path.split(project_path)[-1]

        sys.path.insert(0, project_path)
        sys.path.append(os.path.join(project_path, os.pardir))

        # set environ
        settings_name, ext  = os.path.splitext(os.path.basename(settings_path))
        
        settings_modname = '%s.%s' % (project_name,  settings_name)
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_modname
                                                
        opts.default_proc_name  = settings_modname
        
        # django wsgi app
        return django.core.handlers.wsgi.WSGIHandler()

    main("%prog [OPTIONS] [SETTINGS_PATH]", get_app)
    
def run_paster():
    """ runner used for gunicorn_paster command to launch paster compatible applications 
    (pylons, turbogears2, ...) """
    from paste.deploy import loadapp, loadwsgi

    def get_app(parser, opts, args):
        if len(args) != 1:
            parser.error("No application name specified.")

        config_file = os.path.abspath(os.path.normpath(
                            os.path.join(os.getcwd(), args[0])))

        if not os.path.exists(config_file):
            parser.error("Config file not found.")

        config_url = 'config:%s' % config_file
        relative_to = os.path.dirname(config_file)

        # load module in sys path
        sys.path.insert(0, relative_to)

        # add to eggs
        pkg_resources.working_set.add_entry(relative_to)
        ctx = loadwsgi.loadcontext(loadwsgi.SERVER, config_url,
                                relative_to=relative_to)

        if not opts.workers:
            opts.workers = ctx.local_conf.get('workers', 1)

        if not opts.umask:
            opts.umask = int(ctx.local_conf.get('umask', UMASK))
            
        if not opts.group:
            opts.group = ctx.local_conf.get('group')
        
        if not opts.user:
            opts.user = ctx.local_conf.get('user')
     
        if not opts.bind:
            host = ctx.local_conf.get('host')
            port = ctx.local_conf.get('port')
            if host:
                if port:
                    bind = "%s:%s" % (host, port)
                else:
                    bind = host
                opts.bind = bind

        if not opts.debug:
            opts.debug = (ctx.global_conf.get('debug') == "true")
            
        opts.default_proc_name= ctx.global_conf.get('__file__')

        app = loadapp(config_url, relative_to=relative_to)
        return app

    main("%prog [OPTIONS] pasteconfig.ini", get_app)
    
