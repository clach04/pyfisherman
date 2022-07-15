#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import argparse
import os
import sys

import pychromecast


def play_url(url, ip=None, name=None, content_type=None):
    # get device
    if ip:
        cast = pychromecast.Chromecast(ip)
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
    mc.play_media(url, content_type=content_type)
    mc.block_until_active()
    mc.play()
    


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version, sys.platform))

    parser = argparse.ArgumentParser()
    parser.add_argument('url',
        help='URL or media to play, needs to be supported/listed at https://developers.google.com/cast/docs/media')
    parser.add_argument('--ip',
        help='Optional ip address or hostname')
    parser.add_argument('--name',
        help='Optional Chromecast (friendly) name (might be different to hostname), NOTE ip address takes precedence')
    #args = parser.parse_args()  # FIXME use argv
    args = parser.parse_args(argv[1:])

    play_url(args.url, args.ip, args.name)

    return 0


if __name__ == "__main__":
    sys.exit(main())

