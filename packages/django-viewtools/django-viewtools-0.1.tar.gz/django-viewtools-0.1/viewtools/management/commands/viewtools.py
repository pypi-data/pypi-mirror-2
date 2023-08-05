"""
This gives you some handy tools for playing with views from the command line
"""
from django.test.client import Client
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import simplejson
from django.views import debug
from optparse import make_option
from StringIO import StringIO
import sys
import hotshot
import pdb


class Command(BaseCommand):
    help ="Lets you call up views and get information about the page"

    option_list = BaseCommand.option_list + (
        # Post Data options
        make_option("--post-data", action="store", dest="post_data",
                    help="A json formatted string to send via POST",
                    metavar="STRING"),
        make_option("--post-datafile", action="store", dest="post_data_file",
                    help="A filename to load the json post data from",
                    metavar="FILE"),

        # Debug setting
        make_option("-d", "--debug", action="store_true", dest="debug",
                    help=("Set settings.DEBUG to True, if --debug or"
                          " --no-debug, is not used, Django's setting"
                          " module's DEBUG value will be used")),
        make_option("-n", "--no-debug", action="store_false", dest="debug",
                    help="Set settings.DEBUG to False"),

        # Debugger Settings
        make_option("--pdb", action="store_true", dest="pdb",
                    help="Start pdb before calling the view",
                    default=False),
        make_option("--pm", action="store_true", dest="pdb_pm",
                    help="Fire up pdb when an error occurs",
                    default=False),

        # Profile
        make_option("--profile", action="store", dest="profile",
                    help="dump hotshot profile data to FILE", metavar="FILE"),

        # Quiet
        make_option("-q", "--quiet", action="store_true", dest="quiet",
                    help="Don't output the response from the view"),
        make_option("-m", "--mute", action="store_true", dest="mute",
                    help="Mute stdout and stderr"),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("The only argument for this command is the url")

        # If post-data was given, set it
        data = None
        data_json = None

        if options["post_data"]:
            data_json = options['post_data']

        # if post-datafile was given, read it in
        if options["post_data_file"]:
            data_json = file(options['post_data_file'].read())

        # If we have data, deserialize it
        if data_json:
            data = simplejson.loads(data_json)
        else:
            data = None

        # If debug is given, muck with the settings.DEBUG setting
        if options["debug"] is not None and options['debug']:
            settings.DEBUG = True
        elif options["debug"] is not None:
            settings.DEBUG = False

        # Store pdb_pm incase self.reraise needs it
        self.pdb_pm = options['pdb_pm']

        # If raise errors
        if options['traceback'] or options['pdb_pm']:
            debug.technical_500_response = self.reraise

        def profile_dec(callable):

            def inner(*a, **k):
                prof = hotshot.Profile(options['profile'])
                result = prof.runcall(callable, *a, **k)
                prof.close()
                return result
            return inner

        # If profile in enabled, decorate the call_view
        # with the profiler decorator
        if options['profile']:
            self.call_view = profile_dec(self.call_view)

        # Determine the method we need
        if data:
            method = "POST"
        else:
            method = "GET"
        
        # Get the resp
        resp = self.call_view(args[0],
                              method,
                              data=data,
                              mute=options['mute'],
                              is_pdb=options['pdb'])

        # If not quiet, print the result
        if not options['quiet']:
            print resp.content

    def call_view(self, url, method, data=None, 
                  mute=False, is_pdb=False):
        c = Client()

        # We have to turn off mute if pdb is on
        if is_pdb:
            mute = False
            
        # If we're muted, disable stdout and stderr
        if mute:
            sys.stdout = StringIO()
            sys.stderr = StringIO()

        # Start pdb
        if is_pdb:
            pdb.set_trace()

        try: 
            if method == "GET":
                response = c.get(url)
            elif method == "POST":
                response = c.post(url, data)
        except:
            # Restore the std handlers
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            # Reraise the original error
            raise
        else:
            # Restore the std handlers
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            return response

    def reraise(self, request, exc_type, exc_value, tb):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        if self.pdb_pm:
            print
            print "Exception occured: %s, %s" % (exc_type, exc_value)
            print
            pdb.post_mortem(tb)
        else:
            raise
