from GUI import load_previous_widget as load_previous
from GUI import name_entry_widget as name_entry
from GUI import qt_classes as qt
from GUI import utility_classes as utility
from os import path


class PathEntryWidget(utility.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Select Picture Path', *args, **kwargs)
        self.path_label = qt.Label(self.root,
                                   text='Click the button below to select the path where your pictures\n'
                                        'are stored. Note that this process will work best if all the\n'
                                        'pictures you want sorted are in one path.',
                                   layout=self.gblayout)
        self.path_entry = qt.PushButton(self.root,
                                        text='Select Pictures path',
                                        layout=self.gblayout,
                                        func=self.select_pic_path)
        self.nav_btn_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(self.nav_btn_layout)
        self.returning_btn = qt.PushButton(self.root,
                                           text='I\'m back!',
                                           layout=self.nav_btn_layout,
                                           func=self.go_load_previous)
        self.nav_btn_layout.addSpacing(100)
        self.next_btn = qt.PushButton(self.root,
                                      text='Next',
                                      layout=self.nav_btn_layout,
                                      func=self.go_name_entry)
        self.show()

    @qt.QtCore.Slot()
    def select_pic_path(self, *args, **kwargs):
        self.root.main_pic_path = str(qt.QtWidgets.QFileDialog.getExistingDirectory(self.root,
                                                                                    'Select Main Picture path',
                                                                                    path.expanduser('~')))
        self.root.picsorter_base = path.join(self.root.main_pic_path, f'PicSorter')

    @qt.QtCore.Slot()
    def go_name_entry(self, *args, **kwargs):
        if not self.root.main_pic_path:
            return
        self.load_page(self.root.name_entry_widget,
                       name_entry.NameEntryWidget)

    @qt.QtCore.Slot()
    def go_load_previous(self, *args, **kwargs):
        self.load_page(self.root.go_previous_widget,
                       load_previous.LoadPreviousWidget)