from GUI import path_entry_widget as path_entry
from GUI import qt_classes as qt
from GUI import utility_classes as utility
from os import path, walk


class LoadPreviousWidget(utility.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Load Previous Project', *args, **kwargs)
        self.label = qt.Label(self.root,
                              text='Click the button below to select the PicSorter folder that\n'
                                   'was created last time.',
                              layout=self.gblayout)
        self.path_select = qt.PushButton(self.root,
                                         text='Select Picsorter Directory Path',
                                         layout=self.gblayout,
                                         func=self.get_picsorter_folder)
        self.nav_btn_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(self.nav_btn_layout)
        self.go_back = qt.PushButton(self.root,
                                     text='Back to new',
                                     layout=self.nav_btn_layout,
                                     func=self.back_to_new)
        self.nav_btn_layout.addSpacing(100)
        self.go = qt.PushButton(self.root,
                                text='Go!',
                                layout=self.nav_btn_layout,
                                func=self.go_ahead)

    @qt.QtCore.Slot()
    def get_picsorter_folder(self, *args, **kwargs):
        self.root.picsorter_base = str(qt.QtWidgets.QFileDialog.getExistingDirectory(self.root,
                                                                                     'Select PicSorter Directory path',
                                                                                     path.expanduser('~')))

    @qt.QtCore.Slot()
    def back_to_new(self, *args, **kwargs):
        self.load_page(self.root.path_entry_widget,
                       path_entry.PathEntryWidget)

    @qt.QtCore.Slot()
    def go_ahead(self, *args, **kwargs):
        sample_pics_path = path.join(self.root.picsorter_base, 'sample_pics')
        for root, dirs, files, in walk(sample_pics_path):
            self.root.sample_pic_paths = [path.join(sample_pics_path, x) for x in files]
            break
        self.root.returned = True
        self.root.go()