from tw.api import Widget, JSLink, CSSLink, js_function
from tw.jquery import jquery_js
from tw.forms import MultipleSelectField

__all__ = ["Jqmultiselect"]

# declare your static resources here

jquery_ui_js = JSLink(modname=__name__,
               filename='static/js/jquery-ui-1.8.custom.min.js',
               javascript=[jquery_js])
jquery_multiselect = JSLink(modname=__name__,
               filename='static/js/ui.multiselect.js',
               javascript=[jquery_js, jquery_ui_js])

jquery_ui_css = CSSLink(modname=__name__, filename='static/css/jquery-ui-1.8.2.custom.css')
multiselect_css = CSSLink(modname=__name__, filename='static/css/ui.multiselect.css')


class Jqmultiselect(MultipleSelectField):

    javascript = [jquery_ui_js, jquery_multiselect]
    css = [jquery_ui_css, multiselect_css]

    params = ["sortable", "searchable"]
    sortable = True
    searchable = True

    def __init__(self, id=None, parent=None, children=[], **kw):
        super(Jqmultiselect, self).__init__(id, parent, children, **kw)

    def update_params(self, d):
        """This method is called every time the widget is displayed. It's task
        is to prepare all variables that are sent to the template. Those
        variables can accessed as attributes of d."""
        super(Jqmultiselect, self).update_params(d)
        multi_params = dict(sortable=self.sortable,
                            searchable=self.searchable)
        call = js_function('$("#%s").multiselect' % d.id)(multi_params)
        self.add_call(call)