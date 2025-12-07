from GUI import path_entry_widget as path_entry
from GUI import qt_classes as qt
from GUI import utility_classes as utility
import sys
from Core import face_grab, face_id
from os import mkdir, path, walk
import shutil

# Main window will remain here and the centralWidget will change
class MainWindow(qt.QtWidgets.QMainWindow):
    # Create variables we want to use later, so that they're considered declared in the init
    main_pic_path = None
    names_list = []
    pic_path_dict = {}
    picsorter_path = None
    sample_pic_paths = []
    picsorter_base = None
    returned = False

    # These will hold our widget instances:
    main_splash_widget = None
    path_entry_widget = None
    go_previous_widget = None
    name_entry_widget = None
    photo_select_widget = None
    sample_photo_select_widget = None

    # screen position variables
    wd = 400
    ht = 200
    x = 0
    y = 0


    def __init__(self, main_app, *args, **kwargs):
        self.main_app = main_app
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Simple Pic Sorter')
        # instantiate our main widget, then set it as the Central widget
        # Load our color theme
        file = qt.QtCore.QFile('Darkeum_teal.qss')
        if not file.open(qt.QtCore.QFile.ReadOnly | qt.QtCore.QFile.Text):
            return
        qss = qt.QtCore.QTextStream(file)
        self.setStyleSheet(qss.readAll())
        # show our window
        self.set_center()
        self.setGeometry(self.geometry().x(), self.geometry().y() + 100, self.wd, self.ht)
        self.path_entry_widget = path_entry.PathEntryWidget(self)
        self.setCentralWidget(self.path_entry_widget)

        self.show()
        # Needed so the x will exit the program
        sys.exit(self.main_app.exec())

    @qt.QtCore.Slot()
    def go(self, *args, **kwargs):
        if not self.returned:
            if not path.exists(self.picsorter_base):
                mkdir(self.picsorter_base)
            sample_pics_path = path.join(self.picsorter_base, 'sample_pics')
            if not path.exists(sample_pics_path):
                mkdir(sample_pics_path)
            new_sample_list = []

            for p in self.sample_pic_paths:
                new_p = path.join(sample_pics_path, path.split(p)[1])
                shutil.copyfile(p, new_p)
                new_sample_list.append(new_p)
            self.sample_pic_paths = new_sample_list.copy()
            train_sets_path = path.join(self.picsorter_base, 'train_sets')
            if not path.exists(train_sets_path):
                mkdir(train_sets_path)
            for name, path_list in self.pic_path_dict.items():
                this_path = path.join(train_sets_path, name)
                if not path.exists(this_path):
                    mkdir(this_path)
                i = 0
                for p in path_list:
                    faces = face_grab.extract_faces(p)
                    for face in faces:
                        face.resize((224, 224)).save(path.join(this_path, f'{name}{i}.jpg'))
                        i += 1
        face_id.main(self.picsorter_base, self.sample_pic_paths)

    def set_center(self):
        center = qt.QtGui.QScreen.availableGeometry(qt.QtWidgets.QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
