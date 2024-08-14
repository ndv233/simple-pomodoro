from PyQt6.QtWidgets import QMainWindow, QStatusBar, QVBoxLayout, QWidget
from mainapplication import MainApplication, TodoList
from pyqtgraph.dockarea import *


class MainWindow(QMainWindow):
    def __init__(self, app):

        super().__init__()
        self.app = app
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Window setup
        self.setWindowTitle("pomodoro")
        self.resize(1200, 200)

        # Main Dock for widgets
        dock_area = DockArea(self)
        self.dock1 = Dock('Widget 1', size=(300, 200))
        self.dock2 = Dock('Widget 2', size=(300, 200))
        self.dock1.hideTitleBar()
        self.dock2.hideTitleBar()
        self.dock1.nStyle = """
        Dock > QWidget {
            border: 1px solid #000;
            border-radius 0px;
        }"""
        self.dock2.nStyle = """
        Dock > QWidget {
            border: 1px solid #000;
            border-radius 0px;
        }"""
        self.widget_one = MainApplication()
        self.widget_two = TodoList()
        dock_area.addDock(self.dock1)
        dock_area.addDock(self.dock2, 'right', self.dock1)
        layout.addWidget(dock_area)
        self.dock1.addWidget(self.widget_one)
        self.dock2.addWidget(self.widget_two)
        self.setGeometry(390, 300, 1200, 400)

        # Menus setup
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        settings_menu = file_menu.addAction("&Settings")
        '''settings_menu.triggered.connect(self.openSettingsWindow)'''  # TODO: make function

        view_stats_action = file_menu.addAction("&Stats")
        '''view_stats_action.connect(self.openStatsWindow)'''  # TODO: make function
        quit_action = file_menu.addAction("&Quit")
        quit_action.triggered.connect(self.quitApp)

        # Status bar setup
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("")

    def quitApp(self):
        self.app.quit()

    '''def openSettingsWindow(self):
        self.w = SettingsWindow()
        self.w.show()'''
