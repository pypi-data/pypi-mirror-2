#!/usr/bin/env python2.6
"""a wrapper for the LongURL url expansion service at longurl.org"""

"""
By Matt Wartell

Simple library usage example:

    import longurl

    expander = longurl.LongURL()
    print expander.expand('http://bit.ly/1njFvl')

    or use:
        python longurl.py --help
    for the command line function
"""

import json
import urllib2
import time
import cPickle as pickle
import os.path
import sys
from errno import ENOENT
from optparse import OptionParser
import logging
import textwrap

__all__ = ['LongURL']

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("longurl")
debug = logger.debug
info = logger.info


class Cache(object):
    """stores expirable prior results from longurl across sessions"""

    def __init__(self):
        """only the nil data slots are constructed, late loading is in load()"""
        self.clear()

    def load(self, cachefile='~/.longurl.cache', clear_cache=False):
        """the services listing and succesful lookups are cached
            in a file in the user's home directory or overridden by args
            the cache can be completed cleared if requested"""
        info('Cache.load(%s, %s)' % (cachefile, clear_cache))
        self.store = os.path.expanduser(cachefile)
        self.clear()
        if clear_cache:
            return
        else:
            self._load_pickle()
            self._expire_old_items()

    def clear(self):
        """initializes the cache to nil (thereby clearing it if it existed)"""
        self.services = None
        self.services_born = 0
        self.lookups = {}

    def _expired(self, born, maxlife=60*60*5):
        """returns True if born time is longer than maxlife seconds ago"""
        # default maxlife is 5 hours in seconds
        return born + maxlife < int(time.time())

    def _expire_old_items(self):
        self.get_services()     # services() handles its own expiration
        for short in self.lookups.keys():
            (_, born) = self.lookups[short]
            if self._expired(born):
                debug('%s lookup expired' % short)
                del self.lookups[short]

    def store_services(self, services):
        """stash the list of supported services and mark its born as now"""
        self.services = services
        self.services_born = int(time.time())

    def get_services(self):
        """returns the list of supported services or None if expired or not known"""
        if self._expired(self.services_born):
            debug("services expired")
            self.services_born = 0
            self.services = None
        return self.services

    def store_expansion(self, short, expanded):
        """stash the given translation and mark its born as now"""
        self.lookups[short] = (expanded, int(time.time()))

    def lookup(self, short):
        """returns a cached lookup or None if it is expired or not seen"""
        if short not in self.lookups:
            return None
        (expanded, born) = self.lookups[short]
        if not self._expired(born):
            return expanded
        else:
            debug('%s lookup expired' % short)
            del self.lookups[short]
            return None

    def _load_pickle(self):
        """retrieve the contents of the store if it exists"""
        try:
            with open(self.store, 'rb') as infile:
                self.services_born = pickle.load(infile)
                self.services = pickle.load(infile)
                self.lookups = pickle.load(infile)
            debug('cache loaded')
        except IOError as e:
            if e[0] != ENOENT:
                raise IOError(e[0], '%s: %s' % (self.store, e[1]))
            else:
                # if the store file didn't exist than there is no cache
                self.clear()

    def _store_pickle(self, final=True):
        """save the contents of the cache to the store file"""
        try:
            with open(self.store, 'wb') as outfile:
                pickle.dump(self.services_born, outfile)
                pickle.dump(self.services, outfile)
                pickle.dump(self.lookups, outfile)
            debug('cache stored')
        except IOError as e:
            msg = '%s: error writing cachefile %s: %s' % (sys.argv[0], self.store, e[1])
            # since this method may be called as the last gasp after an unrecoverable
            # exception, at least let the user know that the dump failed.
            # library users who don't want stderr messed with should always call
            # with final set to false
            if final:
                print >> sys.stderr, msg
            raise IOError(e[0], msg)

# poor man's singleton, we want a single. module acessible Cache instance
# but we don't know enough to fully load it until arguments have been
# parsed, so here is the instance (this trick was stolen from the standard
# random.py module)
_cache = Cache()

class LongURL(object):
    """provides small url expansion services courtesy of longurl.org"""

    def __init__(self):
        """create an expander based on current api services"""
        self.host = 'http://api.longurl.org/v2/'
        self.headers = {'User-Agent': 'Python-longurl/1.0'}
        self.services = self._get_services()


    def _get_services(self):
        """returns the list of domains currently translated by longurl"""
        req_url = self.host + 'services?format=json'
        req = urllib2.Request(req_url, headers=self.headers)
        services = json.loads(urllib2.urlopen(req).read())

        # the v2 longurl returns a dictionary of dictionaries for
        # presumed future expansion. the content is currently 
        # redundant or null so we'll just condense it
        domains = []
        for row in services:
            # odd, one entry - digg.com - has a 'regex' key in it which 
            # contains u'http:\\/\\/digg\\.com\\/[^\\/]+$ 
            # which matches only one component paths, I'm going to ignore
            # the whole domain for now
            if row == 'digg.com': continue
            assert services[row]['domain'] == row
            assert not services[row]['regex']
            domains.append(row)

        _cache.store_services(domains)
        return domains

    def expand(self, surl):
        """expand the given url if longurl serves it, returns url if not"""
        # TODO add actual call to actual expander service
        lurl = _cache.lookup(surl)
        if lurl:
            return lurl
        lurl = surl + "/dada-de-dada-da"
        _cache.store_expansion(surl, lurl)
        return lurl


def _parse_args():
    """runs the command line option parser, returns (options, args, help_func)"""
    description = textwrap.dedent("""
        Translates a shortened URL of the form http://bit.ly/flargl into the real
        URL that the service (e.g. bit.ly) would redirect the shortened URL to.
        The translation service is provided courtesy of http://longurl.org (which
        can be reached via http://is.gd/bT7Lm- if you are feeling perverse)""").lstrip()
    usage = 'usage: %prog [options] shortened-url'

    optp = OptionParser(usage=usage, description=description)
    default_cache = '~/.longurl.cache'
    optp.set_defaults(cache_file=default_cache, wipe_cache=False)

    optp.add_option('-l', '--list-services', default=False, action='store_true',
        help='list all the sortening services that can be expanded')
    optp.add_option('-t', '--test-service', default=False, action='store_true',
        help='test if the shortened url belongs to a supported shortening service')
    optp.add_option('-f', '--cache-file', metavar='FILE',
        help='override the default cache-file %s' % default_cache)
    optp.add_option('-W', '--wipe-cache', action='store_true',
        help="clear the cache-file if it exists")
    # TODO reverse the sense of -d before release
    optp.add_option('-d', '--no-debug', action='store_true', default=False,
        help="enable debugging to stderr")
    (options, args) =  optp.parse_args()
    return (options, args, optp.print_help)

def main():
    (options, args, help_func) = _parse_args()

    if options.no_debug:
        logger.setLevel(logging.CRITICAL)

    # get the cache loaded as soon as we can
    _cache.load(options.cache_file, options.wipe_cache)
    longurl = LongURL()

    if len(args) != 1:
        help_func()
        sys.exit(1)

    print longurl.expand(args[0])

    _cache._store_pickle()

if __name__ == '__main__': main()

