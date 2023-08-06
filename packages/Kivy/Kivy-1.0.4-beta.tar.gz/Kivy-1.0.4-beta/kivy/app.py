'''
Application
===========

The :class:`App` class is the base for creating Kivy applications.
Think of it as your main entry point into the Kivy run loop.  In most cases, you
subclass this class and make your own app. You create an instance of your
specific app class and then, when you are ready to start the application's life
cycle, you call your instance's :func:`App.run` method.


Creating an Application by Overriding build()
---------------------------------------------

To initialize your app with a widget tree, override the build() method in
your app class and return the widget tree you constructed.

Here's an example of very simple application that just shows a button:

.. include:: ../examples/application/app_with_build.py
   :literal:

The file is also available in the examples folder at
:file:`kivy/examples/application/app_with_build.py`.

Here, no widget tree was constructed (or if you will, a tree with only the root
node).


Creating an Application via kv File
------------------------------------

You can also use the :doc:`api-kivy.lang` for creating application. The .kv can
contain rules and root widget definitions at the same time. Here is the same
example as the Button one in a kv file.

Contents of 'test.kv':

.. include:: ../examples/application/test.kv
   :literal:

Contents of 'main.py':

.. include:: ../examples/application/app_with_kv.py
   :literal:

See :file:`kivy/examples/application/app_with_kv.py`.

The relation between main.py and test.kv is explained in :func:`App.load_kv`.
'''

from inspect import getfile
from os.path import dirname, join, exists
from kivy.base import runTouchApp, stopTouchApp
from kivy.event import EventDispatcher
from kivy.lang import Builder


class App(EventDispatcher):
    ''' Application class, see module documentation for more information.

    :Events:
        `on_start`:
            Fired when the application is being started (before the
            :func:`~kivy.base.runTouchApp` call.
        `on_stop`:
            Fired when the application stops.
    '''

    def __init__(self, **kwargs):
        super(App, self).__init__()
        self.register_event_type('on_start')
        self.register_event_type('on_stop')
        self.options = kwargs
        self.use_default_uxl = kwargs.get('use_default_uxl', True)
        self.built = False

        #: Root widget set by the :func:`build` method or by the
        #: :func:`load_kv` method if the kv file contains a root widget.
        self.root = None

    def build(self):
        '''Initializes the application; will be called only once.
        If this method returns a widget (tree), it will be used as the root
        widget and added to the window.
        '''
        pass

    def load_kv(self):
        '''This method is invoked the first time the app is being run if no
        widget tree has been constructed before for this app.
        This method then looks for a matching kv file in the same directory as
        the file that contains the application class.

        For example, if you have a file named main.py that contains::

            class ShowcaseApp(App):
                pass

        This method will search for a file named `showcase.kv` in
        the directory that contains main.py. The name of the kv file has to be
        the lowercase name of the class, without the 'App' postfix at the end
        if it exists.

        You can define rules and a root widget in your kv file::

            <ClassName>: # this is a rule
                ...

            ClassName: # this is a root widget
                ...

        There must be only one root widget. See the :doc:`api-kivy.lang`
        documentation for more information on how to create kv files. If your
        kv file contains a root widget, it will be used as self.root, the root
        widget for the application.
        '''
        directory = dirname(getfile(self.__class__))
        clsname = self.__class__.__name__
        if clsname.endswith('App'):
            clsname = clsname[:-3]
        filename = join(directory, '%s.kv' % clsname.lower())
        if not exists(filename):
            return
        root = Builder.load_file(filename)
        if root:
            self.root = root

    def run(self):
        '''Launches the app in standalone mode.
        '''
        if not self.built:
            self.load_kv()
            root = self.build()
            if root:
                self.root = root
        if self.root:
            from kivy.core.window import Window
            Window.add_widget(self.root)
        self.dispatch('on_start')
        runTouchApp()
        self.dispatch('on_stop')

    def stop(self, *largs):
        '''Stop the application.

        If you use this method, the whole application will stop by issuing
        a call to :func:`~kivy.base.stopTouchApp`.
        '''
        stopTouchApp()

    def on_start(self):
        '''Event handler for the on_start event, which is fired after
        initialization (after build() has been called), and before the
        application is being run.
        '''
        pass

    def on_stop(self):
        '''Event handler for the on_stop event, which is fired when the
        application has finished running (e.g. the window is about to be
        closed).
        '''
        pass

