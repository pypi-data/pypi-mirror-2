import unittest

class TestBFGShellCommand(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.bfg.paster import BFGShellCommand
        return BFGShellCommand

    def _makeOne(self):
        return self._getTargetClass()('bfgshell')

    def test_command_ipython_disabled(self):
        command = self._makeOne()
        interact = DummyInteractor()
        app = DummyApp()
        loadapp = DummyLoadApp(app)
        command.interact = (interact,)
        command.loadapp = (loadapp,)
        command.args = ('/foo/bar/myapp.ini', 'myapp')
        class Options(object): pass
        command.options = Options()
        command.options.disable_ipython =True
        command.command(IPShell=None)
        self.assertEqual(loadapp.config_name, 'config:/foo/bar/myapp.ini')
        self.assertEqual(loadapp.section_name, 'myapp')
        self.failUnless(loadapp.relative_to)
        self.assertEqual(len(app.threadlocal_manager.pushed), 1)
        pushed = app.threadlocal_manager.pushed[0]
        self.assertEqual(pushed['registry'], dummy_registry)
        self.assertEqual(pushed['request'].registry, dummy_registry)
        self.assertEqual(interact.local, {'root':dummy_root})
        self.failUnless(interact.banner)
        self.assertEqual(len(app.threadlocal_manager.popped), 1)

    def test_command_ipython_enabled(self):
        command = self._makeOne()
        app = DummyApp()
        loadapp = DummyLoadApp(app)
        command.loadapp = (loadapp,)
        dummy_shell_factory = DummyIPShellFactory()
        command.args = ('/foo/bar/myapp.ini', 'myapp')
        class Options(object): pass
        command.options = Options()
        command.options.disable_ipython = False
        command.command(IPShell=dummy_shell_factory)
        self.assertEqual(loadapp.config_name, 'config:/foo/bar/myapp.ini')
        self.assertEqual(loadapp.section_name, 'myapp')
        self.failUnless(loadapp.relative_to)
        self.assertEqual(len(app.threadlocal_manager.pushed), 1)
        pushed = app.threadlocal_manager.pushed[0]
        self.assertEqual(pushed['registry'], dummy_registry)
        self.assertEqual(pushed['request'].registry, dummy_registry)
        self.assertEqual(dummy_shell_factory.shell.local_ns,{'root':dummy_root})
        self.assertEqual(dummy_shell_factory.shell.global_ns, {})
        self.failUnless('\n\n' in dummy_shell_factory.shell.IP.BANNER)
        self.assertEqual(len(app.threadlocal_manager.popped), 1)

    def test_command_get_app_hookable(self):
        from paste.deploy import loadapp
        command = self._makeOne()
        app = DummyApp()
        apped = []
        def get_app(*arg, **kw):
            apped.append((arg, kw))
            return app
        command.get_app = get_app
        interact = DummyInteractor()
        app = DummyApp()
        command.interact = (interact,)
        command.args = ('/foo/bar/myapp.ini', 'myapp')
        class Options(object): pass
        command.options = Options()
        command.options.disable_ipython =True
        command.command(IPShell=None)
        self.assertEqual(len(app.threadlocal_manager.pushed), 1)
        pushed = app.threadlocal_manager.pushed[0]
        self.assertEqual(pushed['registry'], dummy_registry)
        self.assertEqual(pushed['request'].registry, dummy_registry)
        self.assertEqual(interact.local, {'root':dummy_root})
        self.failUnless(interact.banner)
        self.assertEqual(len(app.threadlocal_manager.popped), 1)
        self.assertEqual(apped, [(('/foo/bar/myapp.ini', 'myapp'),
                                  {'loadapp': loadapp})])

    def test_command_get_root_hookable(self):
        command = self._makeOne()
        interact = DummyInteractor()
        app = DummyApp()
        loadapp = DummyLoadApp(app)
        command.interact = (interact,)
        command.loadapp = (loadapp,)
        root = Dummy()
        apps = []
        def get_root(app):
            apps.append(app)
            return root, lambda *arg: None
        command.get_root =get_root
        command.args = ('/foo/bar/myapp.ini', 'myapp')
        class Options(object): pass
        command.options = Options()
        command.options.disable_ipython =True
        command.command(IPShell=None)
        self.assertEqual(loadapp.config_name, 'config:/foo/bar/myapp.ini')
        self.assertEqual(loadapp.section_name, 'myapp')
        self.failUnless(loadapp.relative_to)
        self.assertEqual(len(app.threadlocal_manager.pushed), 0)
        self.assertEqual(interact.local, {'root':root})
        self.failUnless(interact.banner)
        self.assertEqual(apps, [app])

class TestGetApp(unittest.TestCase):
    def _callFUT(self, config_file, section_name, loadapp):
        from repoze.bfg.paster import get_app
        return get_app(config_file, section_name, loadapp)

    def test_it(self):
        import os
        app = DummyApp()
        loadapp = DummyLoadApp(app)
        result = self._callFUT('/foo/bar/myapp.ini', 'myapp', loadapp)
        self.assertEqual(loadapp.config_name, 'config:/foo/bar/myapp.ini')
        self.assertEqual(loadapp.section_name, 'myapp')
        self.assertEqual(loadapp.relative_to, os.getcwd())
        self.assertEqual(result, app)

class Dummy:
    pass

class DummyIPShellFactory(object):
    def __call__(self, argv, user_ns=None):
        shell = DummyIPShell()
        shell(user_ns, {})
        self.shell = shell
        return shell

class DummyIPShell(object):
    IP = Dummy()
    IP.BANNER = 'foo'
    def __call__(self, local_ns, global_ns):
        self.local_ns = local_ns
        self.global_ns = global_ns

    def mainloop(self):
        pass

dummy_root = Dummy()

class DummyRegistry(object):
    def queryUtility(self, iface, default=None):
        return default

dummy_registry = DummyRegistry()

class DummyInteractor:
    def __call__(self, banner, local):
        self.banner = banner
        self.local = local

class DummyLoadApp:
    def __init__(self, app):
        self.app = app

    def __call__(self, config_name, name=None, relative_to=None):
        self.config_name = config_name
        self.section_name = name
        self.relative_to = relative_to
        return self.app

class DummyApp:
    def __init__(self):
        self.registry = dummy_registry
        self.threadlocal_manager = DummyThreadLocalManager()

    def root_factory(self, environ):
        return dummy_root

class DummyThreadLocalManager:
    def __init__(self):
        self.pushed = []
        self.popped = []
        
    def push(self, item):
        self.pushed.append(item)

    def pop(self):
        self.popped.append(True)
        
