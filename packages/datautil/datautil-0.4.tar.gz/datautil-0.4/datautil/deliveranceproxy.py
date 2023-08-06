'''Use deliverance_ for proxying and re-theming.

.. _deliverance: http://packages.python.org/Deliverance/

Usage requirements (in pip-requirements.txt format)::

    # suggest installing lxml directly
    lxml
    deliverance>=0.3a
    # for urlmap and proxy
    paste
    # for Response
    webob

Example usage::

    dest = 'http://myremotes.ite/'
    mytheme = '<html>....</html>'
    my_deliverance_rules = '<ruleset><theme href="%s" /> ...</ruleset>'
    # or
    # my_deliverance_rules = open('/my/path/to/rules.xml').read()
    deliverance_proxy = create_deliverance_proxy(mytheme, dest,
        my_deliverance_rules)

    # from in wsgi app
    # path on remote destination url you want to proxy to ...
    # you can omit this if local path and remote path are the same
    environ['PATH_INFO'] = '/my_destination_path'
    deliverance_proxy(environ, start_response)
'''
import logging

import paste.urlmap
import deliverance.middleware
import paste.proxy
from webob import Request, Response
from deliverance.middleware import DeliveranceMiddleware, SubrequestRuleGetter
from deliverance.log import PrintingLogger


default_deliverance_rules = \
'''<ruleset>
  <theme href="%s" />
  <!-- These are the default rules for anything with class="default" or no class: -->
  <!-- suppress standard behaviour of copying over head stuff links, html, css
  etc -->
  <rule suppress-standard="1"> 
      <replace content="children:/html/head/title" theme="children:/html/head/title" nocontent="ignore" />

    <replace content="children:#content" theme="children:#content" />
    <!--
    <append content="children:#sidebar" theme="children:#primary" />
    -->
  </rule>
</ruleset>
'''

def create_deliverance_proxy(proxy_base_url, theme_html, rules_xml=None):
    '''Proxy to another url with re-theming using deliverance.

    Based on http://rufuspollock.org/code/deliverance

    :param proxy_base_url: base destination url we are proxying to.
    :param theme_html: string providing html theme to use for re-themeing.
    :param rules_xml: (optional) deliverance rules xml as a string. If not
        provided use `default_deliverance_rules`. For info on rulesets see
        deliverance docs. We require that ruleset support a single
        substitution string '%s' which is used to insert internal mountpoint
        for the them ('/_deliverance_theme.html').
    '''
    theme_url = '/_deliverance_theme.html'
    # use a urlmap so we can mount theme and urlset
    app = paste.urlmap.URLMap()
    # set up theme consistent with our rules file
    app[theme_url] = Response(theme_html)

    if rules_xml:
        rules = rules_xml
    else:
        rules = default_deliverance_rules
    rules = rules % theme_url
    app['/_deliverance_rules.xml'] = Response(rules, content_type="application/xml")

    class MyProxy(object):
        def __init__(self, proxy_base_url):
           self.proxy = paste.proxy.Proxy(proxy_base_url) 
        
        def __call__(self, environ, start_response):
            req = Request(environ)
            res = req.get_response(self.proxy)
            res.decode_content()
            return res(environ, start_response)

    app['/'] = MyProxy(proxy_base_url)
    deliv = DeliveranceMiddleware(app, SubrequestRuleGetter('/_deliverance_rules.xml'),
        PrintingLogger,
        log_factory_kw=dict(print_level=logging.WARNING))
    return deliv

