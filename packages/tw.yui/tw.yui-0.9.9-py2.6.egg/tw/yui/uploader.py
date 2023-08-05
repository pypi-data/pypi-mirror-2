from base import YUICSSLink, YUIJSLink

from widgets import element_js, datasource_js, datatable_js, yahoo_dom_event_js, skin_css

class uploader_js(YUIJSLink):
    javascript = [yahoo_dom_event_js(), element_js(), datasource_js(), datatable_js()]
    css = [skin_css()]
    basename="uploader/uploader"
#    default_suffix=''
