import wx, sys, pickle, wx.aui, os
import Wave
from Wave import images, dbif, grid, MM2, exceptions, metamodel, operations
from Wave.exceptions import WaveIOError

##
# \todo A WaveSession should also contain metamodels.

class WaveSession():

    """Wave session class.
    
       A Wave session records all models, metamodels and names.
    """
    def __init__(self, name_relation_map = {}):
        self.name_relation_map = name_relation_map

    def get(self):
        return self.name_relation_map

    def set(self, relation, name):
        self.name_relation_map[name] = relation

class WaveNotebook(wx.aui.AuiNotebook):
    """Custom WAVE wxPython-Notebook class.
    
    """

    def __init__(self, parent):
        wx.aui.AuiNotebook.__init__(self, parent)

    def new_page(self, grid_table, name = ''):
        page = wx.Panel(self)
        self.AddPage(page, name)
        Wave.grid.WaveGrid(page, grid_table)

## Custom WAVE wxPython-application class.
#
#  \todo Implement a splash-screen.

class WaveApp(wx.App):
    """Custom WAVE wxPython-application class."""

    def __init__(self, redirect = False, filename = None, useBestVisual = False, clearSigInt = True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        frame = MainFrame(None, -1)
        frame.Show(1)
        self.SetTopWindow(frame)
        return True

## Custom WAVE top-level window class.
#
#  \todo Design and implement a component to turn any dbif-style function
#        into an event handler. (e.g. dbif.join --> on_join)
#  \bug  Inconsistent behavior of session saving. On Windows, Wave can 
#        produce .wave files with a different format to those produced
#        on Linux.
#  \todo Implement row deletion for a specified row.
#  \bug  Closing the main window on Windows generates an error.
#  \todo Window title should incorporate name of currently open session.

class MainFrame(wx.Frame):
    """Custom WAVE top-level window class."""

    def __init__(self, parent, id):
        self.size = (600, 600)
        self.title = "WAVE (Whole Architecture Verification)"
        wx.Frame.__init__(self, parent, id, title = self.title, size = self.size)
        self.init_session()
        self.init_panel()
        self.init_notebook()
        self.init_statusbar()
        self.init_toolbar()
        self.init_menus()
        self.init_event_binding()

    def init_session(self):
        self.session = WaveSession()

    def init_panel(self):
        self.panel = wx.Panel(self)

    def init_notebook(self):
        self.notebook = WaveNotebook(self.panel)
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

    def init_statusbar(self):
        self.statusBar = self.CreateStatusBar()

    def init_toolbar(self):
        self.toolbar = self.CreateToolBar()
        self.new_model_toolbar_item = self.toolbar.AddSimpleTool(wx.NewId(), Wave.images.getNewBitmap(), "New", "Long help for 'New'")
        self.toolbar.Realize()

    def init_menus(self):
        self.init_session_menu()
        self.init_models_menu()
        self.init_metamodels_menu()
        self.init_menubar()

    def init_session_menu(self):
        self.session_menu = wx.Menu()
        self.open_session_menu_item = self.session_menu.Append(wx.NewId(), "&Open", "Open")
        self.save_session_menu_item = self.session_menu.Append(wx.NewId(), "&Save", "Save")
        self.exit_menu_item = self.session_menu.Append(wx.NewId(), "E&xit\tCtrl-Q", "Exit")

    def init_models_menu(self):
        self.models_menu = wx.Menu()
        self.new_model_menu_item = self.models_menu.Append(wx.NewId(), "&New relation\tCtrl-N", "Add a new relation to the current model.")
        self.new_row_menu_item = self.models_menu.Append(wx.NewId(), "Add row\tCtrl-R", "Add row to the current relation.")
        self.delete_row_menu_item = self.models_menu.Append(wx.NewId(), "Delete row\tCtrl-X", "Delete row from the current relation.")

    def init_metamodels_menu(self):
        self.metamodels_menu = wx.Menu()
        self.import_metamodel_menu_item = self.metamodels_menu.Append(wx.NewId(), "&Import", "Import")
        self.metamodels_menu.Append(wx.NewId(), "&Export", "Export")

    def init_menubar(self):
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.session_menu, "&Session")
        self.menuBar.Append(self.models_menu, "&Model")
        self.menuBar.Append(self.metamodels_menu, "M&eta-models")
        self.SetMenuBar(self.menuBar)

    def init_event_binding(self):
        self.Bind(wx.EVT_MENU, self.on_close, self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.on_new_row, self.new_row_menu_item)
        self.Bind(wx.EVT_MENU, self.on_new_model, self.new_model_menu_item)
        self.Bind(wx.EVT_TOOL, self.on_new_model, self.new_model_toolbar_item)
        self.Bind(wx.EVT_MENU, self.on_delete_row, self.delete_row_menu_item)
        self.Bind(wx.EVT_MENU, self.on_open_session, self.open_session_menu_item)
        self.Bind(wx.EVT_MENU, self.on_save_session, self.save_session_menu_item)
        self.Bind(wx.EVT_MENU, self.on_import_metamodel, self.import_metamodel_menu_item)

    def current_page(self):
        selection = self.notebook.GetSelection()
        page = self.notebook.GetPage(selection)
        return page

    def current_grid(self):
        current_page = self.current_page()
        children = current_page.GetChildren()
        return children[0]

    def current_grid_table(self):
        return self.current_grid().grid_table

    def get_grid(self, index):
        page = self.notebook.GetPage(index)
        children = page.GetChildren()
        return children[0]

    def get_grid_table(self, index):
        return self.get_grid(index).grid_table

    def update_session(self):
        no_of_pages = self.notebook.GetPageCount()
        for i in range(no_of_pages):
            name = self.notebook.GetPageText(i)
            grid = self.notebook.GetPage(i).GetChildren()[0]
            relation = grid.grid_table.relation
            self.session.set(relation, name)

    def on_open_session(self, event):
        wildcard = "Wave files (*.wave)|*.wave| " \
                   "All files (*.*)|*.* "
        dlg = wx.FileDialog(
                self, message = "Choose a file",
                defaultDir = os.getcwd(), 
                defaultFile = "",
                wildcard = wildcard,
                style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        try:
            file = open(paths[0], 'rb')
        except IOError:
            raise WaveIOError
        dlg.Destroy()        
        self.session = pickle.load(file)
        name_relation_map = self.session.get()
        for name, relation in name_relation_map.iteritems():
            grid_table = Wave.grid.WaveGridTable(relation)
            self.notebook.new_page(grid_table, name)
        file.close()

    def on_save_session(self, event):
        wildcard = "Wave files (*.wave)|*.wave| " \
                   "All files (*.*)|*.* "
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )
        dlg.SetFilterIndex(2)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        try:
            file = open(path, 'wb')
        except IOError:
            raise WAVEIOError
        dlg.Destroy()
        self.update_session()
        pickle.dump(self.session, file)
        file.close()

    def on_close(self, event):
        self.Close(True)

    def on_new_row(self, event):
        grid = self.current_grid()
        grid.AppendRows()
        grid.ForceRefresh()

    def on_new_model(self, event):
        dialog_results = wx.TextEntryDialog(None, "Enter name for new relation:",'Relation name', 'New relation')
        if dialog_results.ShowModal() == wx.ID_OK:
            name = dialog_results.GetValue()
        dialog_results.Destroy()
        relation = Wave.grid.Relation([]) 
        grid_table = Wave.grid.WaveGridTable(relation)
        self.session.set(relation, name)	
        self.notebook.new_page(grid_table, name)

    def on_delete_row(self, event):
        grid = self.current_grid()
        row = grid.GetGridCursorRow()
        grid.DeleteRows(row)
        grid.ForceRefresh()

    def select_page_index(self):
        no_of_pages = self.notebook.GetPageCount()
        choices = [self.notebook.GetPageText(i) for i in range(no_of_pages)]
        dialog_results = wx.SingleChoiceDialog ( None, 'Pick something....', 'Dialog Title', choices )
        if dialog_results.ShowModal() == wx.ID_OK:
            position = dialog_results.GetSelection()
        dialog_results.Destroy()	    
        return position

    def on_import_metamodel(self, event):
        Wave.metamodel.Menu(self, MM2.mm, 'MM2')
        Wave.metamodel.Menu(self, operations.mm, 'operations')

def main():
    app = WaveApp()
    app.MainLoop()
    return 0

if __name__ == '__main__':
    sys.exit(main())

