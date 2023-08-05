
Welcome to tw.jqmultiselect documentation!
==========================================

Contents
--------

.. toctree::
   :maxdepth: 2

tw.jqmultiselect is a tosca widget wrapper around ui.multiselect
a jquery extension which can be found here :

`http://www.quasipartikel.at/multiselect/ <http://www.quasipartikel.at/multiselect/>`_


usage example::

    from tw.forms import TableForm
    from tw.jqmultiselect import Jqmultiselect

    class EditMovieForm(TableForm):
        submit_text = 'Edit Movie'

        fields = [
            Jqmultiselect('actors',
                help_text = 'Please choose the actors of the movie.',
                searchable=True, # default = True
                sortable=True,   # default=True
                ),
                ]



:class:`tw.jqmultiselect.Jqmultiselect`
----------------------------------------------------------

.. autoclass:: tw.jqmultiselect.Jqmultiselect
.. widgetbrowser:: tw.jqmultiselect.samples.DemoJqmultiselect

