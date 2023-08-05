import pkg_resources

__version__ = pkg_resources.get_distribution('ClueDojo').version

DOJO_VERSION = '.'.join(__version__.split('.')[0:3])
GOOGLE_CDN_BASE = 'http://ajax.googleapis.com/ajax/libs/dojo/' + DOJO_VERSION
AOL_CDN_BASE = 'http://o.aolcdn.com/dojo/' + DOJO_VERSION


def _get_cdn_block(base_url, external=False, include_dijit=False):
    dojofile = 'dojo.js'
    if external:
        dojofile = 'dojo.xd.js'

    s = '''
<script type="text/javascript" src="%(base_url)s/dojo/%(dojofile)s"></script>
''' % {'base_url': base_url, 'dojofile': dojofile}

    if include_dijit:
        s += '''
<link rel="stylesheet" href="%(base_url)s/dijit/themes/tundra/tundra.css"
      type="text/css" media="screen" title="dijit tundra css" charset="utf-8">
''' % {'base_url': base_url}

    return s


def get_local_block(base_url, include_dijit=False):
    return _get_cdn_block(base_url, False, include_dijit)


def get_google_cdn_block(include_dijit=False):
    return _get_cdn_block(GOOGLE_CDN_BASE, True, include_dijit)


def get_aol_cdn_block(include_dijit=False):
    return _get_cdn_block(GOOGLE_CDN_BASE, True, include_dijit)
