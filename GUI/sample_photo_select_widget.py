from GUI import photo_select_widget as photo_select
from GUI import qt_classes as qt
from GUI import utility_classes as utility

class SamplePhotoSelect(utility.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Sample Photo Selection', *args, **kwargs)
        self.pic_label = qt.Label(self.root,
                                  text='Click the button below and select 5-10 sample pictures.\n'
                                       'Ideally, each one will have at least 2 of the people you\n'
                                       'have provided names and pictures of. Between all samples,\n'
                                       'you should try to make sure each person is in at least one.',
                                  layout=self.gblayout)
        self.select_btn = qt.PushButton(self.root,
                                        text='Select Sample Photos',
                                        layout=self.gblayout,
                                        func=self.select_photos)
        self.pic_label = qt.Label(self.root,
                                  text='Thumbnails of your sample pictures will show here once you\n'
                                       'have chosen them by clicking the button above',
                                  layout=self.gblayout)
        self.nav_btn_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(self.nav_btn_layout)
        self.back_button = qt.PushButton(self.root,
                                         text='Back',
                                         layout=self.nav_btn_layout,
                                         func=self.back_to_photo_select)
        self.nav_btn_layout.addSpacing(100)
        self.next_button = qt.PushButton(self.root,
                                         text='Next',
                                         layout=self.nav_btn_layout,
                                         func=self.go)
        self.show()

    @qt.QtCore.Slot()
    def select_photos(self, *args, **kwargs):
        dialog = qt.QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.root.main_pic_path)
        dialog.setFileMode(qt.QtWidgets.QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg *.PNG *.JPG *.jpeg *.JPEG)")
        dialog.setViewMode(qt.QtWidgets.QFileDialog.ViewMode.List)
        if dialog.exec():
            self.root.sample_pic_paths = dialog.selectedFiles()

    @qt.QtCore.Slot()
    def go(self, *args, **kwargs):
        if not self.root.sample_pic_paths:
            return
        self.root.go()


    @qt.QtCore.Slot()
    def back_to_photo_select(self, *args, **kwargs):
        self.load_page(self.root.photo_select_widget,
                  photo_select.PhotoSelectWidget)