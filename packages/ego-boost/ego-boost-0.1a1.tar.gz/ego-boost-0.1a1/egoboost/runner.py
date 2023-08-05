# This file is part of the egoboost package which is release under the MIT
# License. You can find the full text of the license in the LICENSE file.
# Copyright (C) 2010 Sebastian Rahlf <basti at redtoad dot de>

import cmd
import os, os.path
import optparse
import re
import sys

import storage
import utils

CONFIG_DIR = os.path.expanduser('~/.ego-boost')
DATABASE = 'downloads.db'

class CommandLine(cmd.Cmd):

    """
    Accepts commands via command line.
    """

    def __init__(self, db, quiet=False):
        cmd.Cmd.__init__(self)
        self.db = db
        self.quiet = quiet

    def default(self, line):
        raise NotImplementedError

    def log(self, msg):
        if not self.quiet:
            print >> sys.stderr, msg

    def do_collect(self, line):
        """
        Collects download information for package::

            collect <package> URL [URL ...]
        """
        SOURCE_REG = {
            'bitbucket' : re.compile('(bit|byte)bucket\.org'),
            'pypi' : re.compile('pypi.python.org'),
            'github' : re.compile('github.com'),
        }
        def guess_source(url):
            "Get source identifier from URL."
            for key, reg in SOURCE_REG.items():
                if reg.search(url):
                    return key
            return None

        parts = line.split()
        package = parts.pop(0)
        for url in parts:
            def subst(mobj):
                "Substitute shortcuts (like 'pypi:...')"
                return {
                    'pypi' : 'http://pypi.python.org/pypi/',
                    'bb' : 'http://bitbucket.org/',
                    'gh' : 'http://github.com/',
                }[mobj.group(1)]
            url = re.sub('(^\w+):(?!//)', subst, url)

            source = guess_source(url)

            self.log('Fetching data from %s...' % url)
            data = utils.get_downloads(url)

            self.db.add(package, data, source)

    def do_export(self, line):
        """
        Exports data to CSV.
        """
        print self.db.tocsv()

def main(argv=sys.argv[1:]):
    """
    Main program.
    """
    # create config dir if not exists
    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)

    parser = optparse.OptionParser()
    parser.add_option('-q', '--quiet', dest='quiet', action='store_true',
          help='Suppress output.', default=False)
    opt, arg = parser.parse_args(argv)

    if len(arg) == 0:
        parser.print_help()
        parser.exit()

    db = storage.DB(os.path.join(CONFIG_DIR, DATABASE))
    command = CommandLine(db, opt.quiet)
    
    try:
        command.onecmd(' '.join(arg))
    except NotImplementedError:
        parser.error('Unknown command!')

if __name__ == '__main__':
    main('collect python-weewar pypi:python-weewar bb:basti/python-weewar --quiet'.split())