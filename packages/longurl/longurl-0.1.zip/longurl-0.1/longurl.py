#!/usr/bin/env python2.6
"""a wrapper for the LongURL url expansion service at longurl.org"""

"""
by matt wartell

Simple library usage example:

    import longurl

    expander = longurl.LongURL()
    print expander.expand('http://bit.ly/1njFvl')

or use:

    python longurl.py --help

for the command line function
"""

# this module relies on the kind generosity of the longurl.org api services
# modifications should follow the "Courteous Usage" requests listed at 
# http://longurl.org/api
# In particular, the original version of this module:
#  1. was informally registered with info@longurl.org
#  2. caches all responses from the service in a cache with timed invalidation
#     and saves the cache in a per-user storage file between invocations.
#     Given that a short-url should have a long-term validity, the current
#     invalidation time is probably too short.
#  3. every http request to longurl.org has a User-Agent field specific to this
#     application
#  4. all URL arguments are URLencoded
#  5. untranslatable (malformed, unserviced) urls are not sent to the service
#
# This satisfies all the conditions requested as of 4 may 2010


from errno import ENOENT
from optparse import OptionParser
import atexit
import cPickle as pickle
import json
import logging
import os.path
import sys
import textwrap
import time
import urllib
import urllib2
import urlparse

__all__ = ['LongURL']


class Cache(object):
    """stores expirable prior results from longurl across sessions"""
    # this probably wants to be nested in LongURL but that's unnecessarily confusing
    # this class isn't exported to library users and so is sorta hidden

    def __init__(self):
        """only the nil data slots are constructed, late loading is in load()"""
        self.clear()
        # if debugging isn't enabled, we'll waste a few cycles generating messages, oh well
        logger = logging.getLogger("longurl.cache")
        self.debug = logger.debug


    def load(self, cachefile='~/.longurl.cache', clear_cache=False):
        """the services listing and succesful lookups are cached
            in a file in the user's home directory or overridden by args
            the cache can be completed cleared if requested"""
        self.debug('Cache.load(%s, %s)' % (cachefile, clear_cache))
        self.storefile = os.path.expanduser(cachefile)
        self.clear()
        if clear_cache:
            return
        else:
            self.read_storefile()
            self.expire_old_items()

    def clear(self):
        """initializes the cache to nil (thereby clearing it if it existed)"""
        self.services = None
        self.services_born = 0
        self.lookups = {}
        self.dirty = False

    def expired(self, born, maxlife=60*60*5):
        """returns True if born time is longer than maxlife seconds ago"""
        # default maxlife is 5 hours in seconds
        return born + maxlife < int(time.time())

    def expire_old_items(self):
        self.get_services()     # services() handles its own expiration
        for short in self.lookups.keys():
            (_, born) = self.lookups[short]
            if self.expired(born):
                self.debug('%s lookup expired' % short)
                del self.lookups[short]
                self.dirty = True

    def store_services(self, services):
        """stash the list of supported services and mark its born as now"""
        self.services = services
        self.services_born = int(time.time())
        self.dirty = True

    def get_services(self):
        """returns the list of supported services or None if expired or not known"""
        if self.expired(self.services_born):
            self.debug("services expired")
            self.services_born = 0
            self.services = None
            self.dirty = True
        return self.services

    def store_expansion(self, short, expanded):
        """stash the given translation and mark its born as now"""
        self.lookups[short] = (expanded, int(time.time()))
        self.dirty = True

    def lookup(self, short):
        """returns a cached lookup or None if it is expired or not seen"""
        if short not in self.lookups:
            return None
        (expanded, born) = self.lookups[short]
        if not self.expired(born):
            return expanded
        else:
            self.debug('%s lookup expired' % short)
            del self.lookups[short]
            self.dirty = True
            return None

    def list_translations(self):
        """convenience function for dumping the cached translations"""
        return [(surl, self.lookups[surl][0]) for surl in sorted(self.lookups.keys())]

    def read_storefile(self):
        """retrieve the contents of the storefile if it exists"""
        try:
            with open(self.storefile, 'rb') as infile:
                self.services_born = pickle.load(infile)
                self.services = pickle.load(infile)
                self.lookups = pickle.load(infile)
            self.dirty = False
            self.debug('cachefile loaded')
        except IOError as e:
            if e[0] != ENOENT:
                raise IOError(e[0], '%s: %s' % (self.storefile, e[1]))
            else:
                # if the store file didn't exist than there is no cache and no exception
                self.clear()


    def write_storefile(self, final=True):
        """save the contents of the cache to the store file"""
        if not self.dirty:
            self.debug('cache is not dirty so cachefile not written')
            return
        try:
            with open(self.storefile, 'wb') as outfile:
                pickle.dump(self.services_born, outfile)
                pickle.dump(self.services, outfile)
                pickle.dump(self.lookups, outfile)
            self.debug('cachefile written')
            self.dirty = False
        except IOError as e:
            msg = '%s: error writing cachefile %s: %s' % (sys.argv[0], self.storefile, e[1])
            # since this method may be called as the last gasp after an unrecoverable
            # exception, at least let the user know that the dump failed.
            # library users who don't want stderr messed with should always call
            # with final set to false
            if final:
                print >> sys.stderr, msg
            raise IOError(e[0], msg)

# poor man's singleton, we want a single. module acessible Cache instance
# but we don't know enough to fully load it until arguments have been
# parsed, so here is the instance (this hack was stolen from the standard
# random.py module)
_cache = Cache()

class LongURL(object):
    """provides small url expansion services courtesy of longurl.org"""

    def __init__(self):
        """create an expander based on current api services"""
        self.host = 'http://api.longurl.org/v2/'
        self.headers = {'User-Agent': 'Python-longurl/1.0'}
        self.services = self.get_services()
        logger = logging.getLogger("longurl")
        self.debug = logger.debug


    def get_services(self):
        """returns the list of domains currently translated by longurl"""
        service_list = _cache.get_services()
        if service_list:
            return service_list

        req_url = self.host + 'services?format=json'
        req = urllib2.Request(req_url, headers=self.headers)
        services = json.loads(urllib2.urlopen(req).read())

        # the v2 longurl api returns a dictionary of dictionaries for
        # presumed future expansion. the content is currently 
        # redundant or null so we'll just condense it
        domains = []
        for row in services:
            # odd, one entry - digg.com - has a 'regex' key in it which 
            # contains u'http:\\/\\/digg\\.com\\/[^\\/]+$ 
            # which matches only single component paths, I'm going to ignore
            # the whole domain for now
            if row == 'digg.com': continue
            assert services[row]['domain'] == row
            assert not services[row]['regex']
            domains.append(row)

        _cache.store_services(domains)
        return domains

    def get_expansions(self):
        """returns a list of tuples containing all discovered translations remembered"""
        return _cache.list_translations()

    def expandable(self, surl):
        """returns a quoted surl if the service can in principle expand surl
           based on textual analysis and matching against known services"""
        if not surl.startswith('http://') and not surl.startswith('https://'):
            self.debug('service only handles http and https not %r' % surl)
            return False

        parts = urlparse.urlparse(surl)
        if parts.netloc not in self.services:
            self.debug('service %r not supported' % parts.netloc)
            return False

        if parts.params or parts.query or parts.fragment:
            self.debug('url %r has components not expected of a surl' % surl)
            return False

        if not parts.path:
            self.debug('url %r has no path' % surl)
            return False

        # it could probably be claimed that a multi-component path is non-shortened
        # and shouldn't be processed for now we'll let it slide
        if parts.path.count('/') > 1:
            self.debug('url %r has a multi-part path' % surl)
            pass

        return urllib.quote_plus(surl)

    def expand(self, surl, qurl=None):
        """expand the given surl if longurl.org serves it, returns surl if not.
           qurl is the quoted form of surl already computed by expandable() or
           will be obtained if qurl is None"""

        # if we have remembered this expansion, just return it
        lurl = _cache.lookup(surl)
        if lurl:
            return lurl

        # unduly tricky logic here: the usual calling sequence is expandable()
        # then expand(). if you've already called expandable() you have its result
        # which is either a quoted surl or False. if you haven't called expandable()
        # you don't have a qurl so expand gets one for you. all this to save a
        # redundant call to expandable(), probably not worth the comment
        if qurl is None:
            qurl = self.expandable(self, surl)
        if not qurl:
            return surl

        # get the expansion 
        try:
            req_url = self.host + 'expand?format=json&url=' + qurl
            req = urllib2.Request(req_url, headers=self.headers)
            lookup = json.loads(urllib2.urlopen(req).read())
            assert lookup['long-url']
        except urllib2.HTTPError as e:
            msg = ('http error %r when asking for %r' % (e, qurl))
            self.debug(msg)
            return surl
        except urllib2.URLError as e:
            msg = ('url error %r when asking for %r' % (e, qurl))
            self.debug(msg)
            return surl

        lurl = lookup['long-url']
        _cache.store_expansion(surl, lurl)
        return lurl

#
# these command line functions _parse_args() and main() could be hoisted out of this
# library module if one was a stickler for things like that, but I'm not
#

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
    optp.add_option('-k', '--list-known', default=False, action='store_true',
        help='list all cached translations')
    optp.add_option('-f', '--cache-file', metavar='FILE',
        help='override the default cache-file %s' % default_cache)
    optp.add_option('-W', '--wipe-cache', action='store_true',
        help="clear the cache-file if it exists")
    optp.add_option('-d', '--debug', action='store_true', default=False,
        help="enable debug logging to stderr")
    (options, args) =  optp.parse_args()

    # option conflicts like "-l -t" or "-l shortened-url" are handled by
    # implicit precdence 

    return (options, args, optp.print_help)

def main():
    (options, args, help_func) = _parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    # get the cache loaded as soon as we can and arrange to dump on exit
    _cache.load(options.cache_file, options.wipe_cache)
    atexit.register(_cache.write_storefile)
    longurl = LongURL()

    if options.list_services:
        for domain in sorted(longurl.get_services()):
            print domain
        sys.exit(0)

    if options.list_known:
        for (surl, lurl) in longurl.get_expansions():
            print surl, lurl
        sys.exit(0)

    if len(args) != 1:
        help_func()
        sys.exit(1)
    surl = args[0]

    qurl = longurl.expandable(surl)

    if options.test_service:
        if qurl:
            print surl, 'is expandable'
            sys.exit(0)
        else:
            print surl, 'is not expandable'
            sys.exit(1)

    if qurl:
        print longurl.expand(surl, qurl)
    else:
        print surl


if __name__ == '__main__': main()

