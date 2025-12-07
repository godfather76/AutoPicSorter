from __future__ import with_statement

from GUI import main_app
from sys import argv

def main():
    # instantiate our app with sys.argv
    app = main_app.qt.QtWidgets.QApplication(argv)
    # instantiate main window, passing in our app instance
    window = main_app.MainWindow(app)
    # Show the window
    window.show()
    # Execute the app
    app.exec()


if __name__ == '__main__':
    main()

    # with open(b'/home/ike/PycharmProjects/MLGame/GUI/') as f1:
    #     with open(filename2) as f2:
    #         if f1.read() == f2.read():
    #