# pyfisherman

pyfisherman casts media to a Chromecast device

For the latest version see https://github.com/clach04/pyfisherman

## Getting Started

    python -m pip install -r requirements.txt

## Usage

    $ ./fisherman.py
    Python 3.8.4 (default, Feb 23 2022, 19:16:17)
    [GCC 6.3.0 20170516] on linux
    pychromecast.version '0.7.6'
    usage: fisherman.py [-h] [--ip IP] [--name NAME] [--auto_url_prefix AUTO_URL_PREFIX] [--file_prefix_remove FILE_PREFIX_REMOVE] urls [urls ...]
    fisherman.py: error: the following arguments are required: urls

Where IP is an ip address and NAME is the Chromecast name.

## Questions no one asked that are plausible FAQs

Why?

To play media from any webserver, optionally using only file names (not URLs) and using that existing server.

Alternatives?

  * https://github.com/skorokithakis/catt
  * https://github.com/dohliam/stream2chromecast
  * https://github.com/vishen/go-chromecast
  * https://github.com/xat/castnow
