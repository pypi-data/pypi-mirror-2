import cluedojo
from cluedojo import wsgiapp


template = '''

<html>
  <head>
    %(dojo_block)s
    <title>Test App</title>
<script>
dojo.require('dijit.Dialog');

dojo.addOnLoad(function() {
    var dialog = new dijit.Dialog({title: 'Test Dialog',
                                   content: 'Hello World!',
                                   style: 'width: 300px'});
    dialog.show();
});
</script>

  </head>
  <body class="tundra">
  </body>
</html>

'''


dojoapp = wsgiapp.make_app({})


def adjust_script_path(environ):
    '''Pop the first part of the PATH_INFO and append it to SCRIPT_NAME'''

    newenv = dict(environ)
    pathinfo = newenv['PATH_INFO'].split('/')
    if pathinfo[0] == '':
        pathinfo = pathinfo[1:]
    scriptname = newenv['SCRIPT_NAME'].split('/')
    if len(pathinfo) > 1:
        scriptname.append(pathinfo[0])
        pathinfo = pathinfo[1:]
    newenv['SCRIPT_NAME'] = '/'.join(scriptname)
    newenv['PATH_INFO'] = '/'.join(pathinfo)
    return newenv


def demo_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])

    path = environ['PATH_INFO']

    if path == '/':
        block = cluedojo.get_local_block(base_url='/dojobase',
                                         include_dijit=True)
        return [template % {'dojo_block': block}]
    elif path.startswith('/dojobase/'):
        return dojoapp(adjust_script_path(environ), start_response)
    elif path == '/external':
        return [template % {'dojo_block': cluedojo.get_google_cdn_block(True)}]
    else:
        start_response('404 Not Found', [])
        return []


def make_app(global_conf={}):
    return demo_app
