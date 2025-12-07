from functools import partial
from GUI import name_entry_widget as name_entry
from GUI import sample_photo_select_widget as sample_photo_select
from GUI import qt_classes as qt
from GUI import utility_classes as utility


class PhotoSelectWidget(utility.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Select Photos', *args, **kwargs)
        # Create dictionary of buttons with labels.
        self.name_btn_dict = {}
        for i,name in enumerate(self.root.names_list):
            self.name_btn_dict[name] = {'btn': qt.PushButton(self.root,
                                                       text=f'{name}',
                                                       layout=self.gblayout,
                                                       func=partial(self.launch_selection, name)),
                                        'label': qt.Label(self.root,
                                                            text=f'{name}\'s pictures will populate here once they have been\n'
                                                                 f'chosen by clicking the button above.',
                                                            layout=self.gblayout)}

        self.nav_btn_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(self.nav_btn_layout)
        self.back_button = qt.PushButton(self.root,
                                         text='Back',
                                         layout=self.nav_btn_layout,
                                         func=self.back_to_names)
        self.next_button = qt.PushButton(self.root,
                                         text='Next',
                                         layout=self.nav_btn_layout,
                                         func=self.go_sample_photo_select)
        self.show()

    @qt.QtCore.Slot()
    def back_to_names(self, *args, **kwargs):
        self.load_page(self.root.name_entry_widget,
                       name_entry.NameEntryWidget)

    @qt.QtCore.Slot()
    def go_sample_photo_select(self, *args, **kwargs):
        for name in self.root.names_list:
            try:
                if not self.root.pic_path_dict[name]:
                    return
            except KeyError:
                return
        self.load_page(self.root.sample_photo_select_widget,
                       sample_photo_select.SamplePhotoSelect)

    @qt.QtCore.Slot()
    def launch_selection(self, name, *args, **kwargs):
        dialog = qt.QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.root.main_pic_path)
        dialog.setFileMode(qt.QtWidgets.QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg *.PNG *.JPG)")
        dialog.setViewMode(qt.QtWidgets.QFileDialog.ViewMode.List)
        if dialog.exec():
            self.root.pic_path_dict[name] = dialog.selectedFiles()

        # FOR ADDING PICS TO THE LABEL; NEEDS WORK
        # for photo_path in self.root.pic_path_dict[name]:
        #     try:
        #         pixmap = qt.QtGui.QPixmap(photo_path)
        #         if pixmap.isNull():
        #             print("Error: Could not load image. Check the path.")
        #         else:
        #             # Scale the pixmap to fit the label, maintaining aspect ratio
        #             # scaled_pixmap = pixmap.scaled(self.name_btn_dict[name]['label'].size(),
        #             #                               qt.QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        #             #                               qt.QtCore.Qt.TransformationMode.SmoothTransformation)
        #             self.name_btn_dict[name]['label'].setPixmap(pixmap)
        #             self.name_btn_dict[name]['label'].setScaledContents(True)  # Ensure the image scales with the label
        #     except Exception as e:
        #         print(f"An error occurred: {e}")