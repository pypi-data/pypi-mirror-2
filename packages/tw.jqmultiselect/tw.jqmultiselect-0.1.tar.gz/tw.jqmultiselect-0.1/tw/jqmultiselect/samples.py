"""
Here you can create samples of your widgets by providing default parameters,
inserting them in a container widget, mixing them with other widgets, etc...
These samples will appear in the WidgetBrowser

See http://toscawidgets.org/documentation/WidgetBrowser for more information
"""

from tw.forms import TableForm
from tw.jqmultiselect import Jqmultiselect


class DemoJqmultiselect(TableForm):
    demo_for = Jqmultiselect

    fields = [
        Jqmultiselect('data',
            help_text = 'Please choose the data you want.',
            searchable=True, # default = True
            sortable=True,   # default=True
            options = ['foo', 'bar', 'baz']

            ),
            ]

