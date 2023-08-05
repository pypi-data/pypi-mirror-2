
import gtk
from zope import interface
from gaphor.core import inject, action, build_action_group
from gaphor.interfaces import IService, IActionProvider
from gaphor.storage import storage, parser
from gaphor.UML.elementfactory import ElementChangedEventBlocker
from gaphor.application import Application

class GaphorModelImport(object):
    
    interface.implements(IService, IActionProvider)

    gui_manager = inject('gui_manager')
    file_manager = inject('file_manager')
    element_factory = inject('element_factory')

    menu_xml = """
      <ui>
        <menubar action="mainwindow">
          <menu action="file">
            <menu action="file-import">
              <menuitem action="file-import-model" />
            </menu>
          </menu>
        </menubar>
      </ui>"""
    
    def __init__(self):
        self.action_group = build_action_group(self)

    def init(self, app):
        pass

    def shutdown(self):
        pass
        
    @action(name='file-import-model', label='Gaphor Model')
    def execute(self):
        filename = self.file_manager._open_dialog("Model Import")
        loader = parser.GaphorLoader()
        for percentage in parser.parse_generator(filename, loader):
            pass
        elements = loader.elements
        gaphor_version = loader.gaphor_version
        Application.register_subscription_adapter(ElementChangedEventBlocker)
        for percentage in storage.load_elements_generator(elements, self.element_factory, gaphor_version):
            pass
        Application.unregister_subscription_adapter(ElementChangedEventBlocker)
