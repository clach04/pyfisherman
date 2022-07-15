#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import argparse
import os
import sys
try:
    # py3
    from urllib.parse import quote
except ImportError:
    # py2
    from urllib import quote

import pychromecast  # pip install pychromecast==7.3.0  # PyChromecast === 7.3.0 fine, 12.1.4 has new API


def play_url(urls, ip=None, name=None, content_type=None, auto_url_prefix=None, file_prefix_remove=None):
    file_prefix_remove_len = 0
    if file_prefix_remove:
        #file_prefix_remove = os.path.abspath(file_prefix_remove) + '/'
        file_prefix_remove = os.path.abspath(file_prefix_remove)
        # if auto_url_prefix ends with '/' and file_prefix_remove does not....
        file_prefix_remove = file_prefix_remove + '/'
        file_prefix_remove_len = len(file_prefix_remove)

    def filename2url(url):
        url = os.path.abspath(url)
        #print('\t' + url)
        if file_prefix_remove and url.startswith(file_prefix_remove):
            url = url[file_prefix_remove_len:]
        #print('\t' + url)
        if auto_url_prefix:
            #print('\t' + auto_url_prefix + url)
            #url = auto_url_prefix + url
            url = auto_url_prefix + quote(url)
        return url

    url_iter = iter(urls)
    url = filename2url(next(url_iter))

    # get device
    if ip:
        # NOTE See https://github.com/home-assistant-libs/pychromecast/issues/611
        # Also see  https://github.com/home-assistant-libs/pychromecast/issues/290 which prevents checking version at runtime
        cast = pychromecast.Chromecast(ip)  # older version required
        # either cast = pychromecast.Chromecast(pychromecast.get_chromecast_from_host(ip))
        # or more likely pychromecast.get_listed_chromecasts()
    elif name:
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[name])
        if not chromecasts:
            print('No chromecast with name "{}" discovered'.format(name))
            return
        cast = chromecasts[0]
    else:
        # just grab the first one we find
        chromecasts, browser = pychromecast.get_listed_chromecasts()
        if not chromecasts:
            print('No chromecasts discovered')
            return
        cast = chromecasts[0]
    cast.wait()

    content_type = content_type or 'audio/mp3'
    mc = cast.media_controller
    print(url)
    mc.play_media(url, content_type=content_type)  # replace current playing media with this
    mc.block_until_active()
    mc.play()
    try:
        while 1:
            url = filename2url(next(url_iter))
            print(url)
            mc.play_media(url, content_type=content_type, enqueue=True)
    except StopIteration:
        # done
        pass



def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version, sys.platform))  # known to work with pychromecast.version '0.7.6'
    print('pychromecast.version %r' % pychromecast.__version__)

    parser = argparse.ArgumentParser()
    parser.add_argument('urls',
        nargs='+',
        help='URLs or media to play, needs to be supported/listed at https://developers.google.com/cast/docs/media')
    parser.add_argument('--ip',
        help='Optional ip address or hostname')
    parser.add_argument('--name',
        help='Optional Chromecast (friendly) name (might be different to hostname), NOTE ip address takes precedence')
    parser.add_argument('--auto_url_prefix',
        help='Optional URL to prefix with each parameter that does not start with http/https')
    parser.add_argument('--file_prefix_remove',
        help='Optional pathname to remove from prefix of any file pathnames that are passed in (rather than URLs')
    args = parser.parse_args(argv[1:])

    play_url(args.urls, args.ip, args.name, auto_url_prefix=args.auto_url_prefix, file_prefix_remove=args.file_prefix_remove)

    return 0


if __name__ == "__main__":
    sys.exit(main())

