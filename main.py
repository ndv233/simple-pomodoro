from PyQt6.QtWidgets import QApplication
import sys
from mainwindow import MainWindow


def main():
    # Initialise application
    app = QApplication(sys.argv)

    # Read style sheet file
    style_sheet = open("Styles/styleSheet.css", "r").read()
    app.setStyleSheet(style_sheet)

    # Initialise main window
    main_app = MainWindow(app)
    main_app.show()
    app.exec()


if __name__ == "__main__":
    main()
