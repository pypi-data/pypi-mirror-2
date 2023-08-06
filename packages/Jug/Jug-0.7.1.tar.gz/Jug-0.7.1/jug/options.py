# -*- coding: utf-8 -*-
# Copyright (C) 2008-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
'''
Options

Variables
---------
- jugdir: main jug directory.
- jugfile: filesystem name for the Jugfile
- cmd: command to run.
- aggressive_unload: --aggressive-unload
- invalid_name: --invalid
- argv: Arguments not captured by jug (for script use)
- print_out: Print function to be used for output (behaves like Python3's print)
'''
from __future__ import division
import logging
import string
import sys

from .p3 import nprint

jugdir = 'jugdata'
jugfile = 'jugfile.py'
cmd = None
aggressive_unload = False
invalid_name = None
argv = None
print_out = nprint
status_mode = 'no-cached'

_Commands = (
    'execute',
    'status',
    'check',
    'sleep-until',
    'stats',
    'cleanup',
    'count',
    'invalidate',
    'shell',
    )
_usage_string = \
'''jug SUBCOMMAND JUGFILE OPTIONS...

Subcommands
-----------
   execute:      Execute tasks
   status:       Print status
   check:        Returns 0 if all tasks are finished. 1 otherwise.
   sleep-until:  Wait until all tasks are done, then exit.
   counts:       Simply count tasks
   cleanup:      Cleanup
   invalidate:   Invalidate the results of a task
   shell:        Run a shell after initialization

General Options
---------------
--jugdir=JUGDIR
    Directory in which to save intermediate files
--verbose=LEVEL
    Verbosity level ('DEBUG', 'INFO', 'QUIET')

execute OPTIONS
---------------
--aggressive-unload
    Aggressively unload data from memory
--pdb
    Call python debugger on errors

invalidate OPTIONS
------------------
--invalid=TASK-NAME
    Task name to invalidate


Examples
--------

  jug status script.py
  jug execute script.py &
  jug execute script.py &
  jug status script.py
'''

def usage():
    '''
    usage()

    Print an usage string and exit.
    '''
    import sys
    print _usage_string
    sys.exit(1)

def parse():
    '''
    options.parse()

    Parse the command line options and set the option variables.
    '''
    import optparse
    global jugdir, jugfile, cmd, aggressive_unload, invalid_name, argv, status_mode, pdb
    parser = optparse.OptionParser()
    parser.add_option('--aggressive-unload',action='store_true',dest='aggressive_unload',default=False)
    parser.add_option('--invalid',action='store',dest='invalid_name',default=None)
    parser.add_option('--jugdir',action='store',dest='jugdir',default='jugdata/')
    parser.add_option('--verbose',action='store',dest='verbosity',default='QUIET')
    parser.add_option('--cache', action='store_true', dest='cache', default=False)
    parser.add_option('--pdb', action='store_true', dest='pdb', default=False)
    options,args = parser.parse_args()
    if not args:
        usage()
        return

    cmd = args.pop(0)
    jugfile = 'jugfile.py'
    if args:
        jugfile = args.pop(0)

    if cmd not in _Commands:
        usage()
        return
    if options.invalid_name and cmd != 'invalidate':
        usage()
        return
    if cmd == 'invalidate' and not options.invalid_name:
        usage()
        return
    try:
        nlevel = {
            'DEBUG' : logging.DEBUG,
            'INFO' : logging.INFO,
        }[string.upper(options.verbosity)]
        root = logging.getLogger()
        root.level = nlevel
    except KeyError:
        pass

    aggressive_unload = options.aggressive_unload
    invalid_name = options.invalid_name
    argv = args
    sys.argv = [jugfile] + args
    status_mode = ('cached' if options.cache else 'no-cached')
    jugdir = options.jugdir
    pdb = options.pdb


