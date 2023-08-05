import os
import time
import imp
from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.daemonize import become_daemon
from django.utils.importlib import import_module

from skypehub.utils import get_skype, SKYPE_HOOK_OPTIONS

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--daemonize', action='store_true',
                dest='daemonize', help='daemonize bot.'),
        make_option('--pidfile', dest='pidfile', default=None,
                help='create pid file.'),
    )
    help = "run skype bot."

    def handle(self, *args, **options):
        skype_options = getattr(settings, 'SKYPE_HOOK_OPTIONS', SKYPE_HOOK_OPTIONS)
        skype = get_skype(**skype_options)

        # --daemonize
        if options['daemonize']:
            become_daemon()

        # --pidfile
        if options['pidfile']:
            pidfile = open(options['pidfile'], 'w')
            pidfile.write('%d' % os.getpid())
            pidfile.close()

        from skypehub.handlers import on_message

        # load module
        for app in settings.INSTALLED_APPS:
            try:
                app_path = import_module(app).__path__
            except AttributeError:
                continue
            try:
                imp.find_module('skypebot', app_path)
            except ImportError:
                continue
            import_module("%s.skypebot" % app)

        # attach skype
        on_message.skype = skype
        skype.OnMessageStatus = on_message.dispatch

        skype.Attach()
        while True:
            time.sleep(1)
