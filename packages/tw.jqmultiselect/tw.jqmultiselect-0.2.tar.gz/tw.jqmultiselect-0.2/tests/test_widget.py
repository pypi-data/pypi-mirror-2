from tw.core.testutil import WidgetTestCase
from tw.jqmultiselect import *

class TestWidget(WidgetTestCase):
    # place your widget at the TestWidget attribute
    TestWidget = Jqmultiselect
    # Initilization args. go here
    widget_kw = {"options":["foo", "bar", "baz"]}

    def test_render(self):
        # Asserts 'foo' and 'test' (the test widget's id) appear in rendered
        self.assertInOutput(['foo', 'bar', 'baz'])
        # Asserts 'ohlalala' does not appear in rendered string when render
        # is called without args
        self.assertNotInOutput(['ohlalala'])
        self.assertInDynamicCalls(['multiselect', 'searchable', 'sortable'])
