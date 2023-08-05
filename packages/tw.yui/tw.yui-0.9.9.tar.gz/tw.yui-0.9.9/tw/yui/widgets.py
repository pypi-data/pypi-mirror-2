from tw.api import Widget, JSLink, CSSLink

from base import YUICSSLink, YUIJSLink
#from yuitest import *

# declare your static resources here

## JS dependencies can be listed at 'javascript' so they'll get included
## before
# my_js = JSLink(modname=__name__,
#                filename='static/yui.js', javascript=[])

# my_css = CSSLink(modname=__name__, filename='static/yui.css')

class element_js(YUIJSLink):
    basename="element/element"
    default_suffix='beta-min'

class datasource_js(YUIJSLink):
    basename="datasource/datasource"
#    default_suffix=''

class datatable_js(YUIJSLink):
    basename="datatable/datatable"
#    default_suffix=''

class json_js(YUIJSLink):
    basename='/json/json'

class connection_js(YUIJSLink):
    basename='connection/connection'

class yahoo_dom_event_js(YUIJSLink):
    basename="yahoo-dom-event/yahoo-dom-event"
    default_suffix=''

class skin_css(YUICSSLink):
    basename="assets/skins/sam/skin"
    default_suffix=""


