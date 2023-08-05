#!/usr/bin/env python
''' broken_since decorator and nose plugin to generate the report '''

import os
from warnings import warn
from nose.plugins.base import Plugin
__version__ = "0.1.1"

_broken_functions = {}

class BrokenSinceDetail(Plugin):
    ''' Plugin that overrides .report() '''

    def options(self, parser, env=os.environ):
        ''' add --broken-since option to get a broken_since report after 
            all unittest have been ran '''
        parser.add_option(
                "--broken-since",
                action="store_true",
                default=env.get('NOSE_BROKEN_SINCE') or False,
                dest="show_broken_report", help="add broken since report")


    def configure(self, options, config):
        ''' enable report if option --broken-since is used '''
        self.enabled = options.show_broken_report
        self.config = config


    def report(self, stream):
        ''' create a summary broken_since report '''
        stream.write('------------ Broken since report ----------------\n')
        stream.write("%s broken_since unittests:\n" % 
                     len(_broken_functions) )
        
        for i, fct in enumerate(_broken_functions):
            record = _broken_functions[fct]
            stream.write("%s - %s\nbroken since %s by %s -> %s\n" 
                         % (i + 1, fct, record['version'], record['user'], 
                            record['reason']))

def broken_since(version, user, reason):
    ''' broken_since decorator that is used to ensure broken unittests
        are skipped but recorded for a summary report at the end of
        nosetest run'''
    
    def decorator(function):
        ''' the broken decorator '''
        record = dict(version=version, user=user, reason=reason)
        _broken_functions[function.__name__] = record

        warn("Not running %s.%s: it's broken since %s because"
             " %r" % (function.__module__, function.__name__, version, reason),
             stacklevel=2)

        # replace the test with a no-op function
        return lambda x: None
    return decorator
