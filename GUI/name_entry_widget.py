from GUI import path_entry_widget as path_entry
from GUI import photo_select_widget as photo_select
from GUI import qt_classes as qt
from GUI import utility_classes as utility


class NameEntryWidget(utility.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Enter Names', *args, **kwargs)
        self.entry_rows = []
        if self.root.names_list:
            self.row_count = len(self.root.names_list)
        else:
            self.row_count = 1
        # A label explaining what to do
        self.label = qt.Label(self.root,
                 text='To begin, enter the names of the people you want to sort\n'
                      'pictures of in the slots below. Add or subtract rows as\n'
                      'needed using the arrow buttons. When you are satisfied,\n'
                      'click Next.',
                 alignment=qt.QtCore.Qt.AlignLeft,
                 layout=self.gblayout)
        # Add a vertical box layout in which to place buttons added by the user. This makes it
        # so adding and subtracting rows is much easier and they align nicely
        self.line_layout = qt.QtWidgets.QVBoxLayout()
        self.gblayout.addLayout(self.line_layout)
        # Create a dictionary of lines. The first one is called main_line and subsequent lines are numbered by
        # which row they are (ie the second line is labeled 2); the additional lines are added in a button function
        # below.
        # The value of each is an instance of our LineEdit widget.
        if not self.root.names_list:
            self.entry_rows.append(qt.LineEdit(self.root,
                                               placeholderText='Enter a name here',
                                               layout=self.line_layout))
        else:
            for name in self.root.names_list:
                self.entry_rows.append(qt.LineEdit(self.root,
                                                   text=f'{name}',
                                                   layout=self.line_layout))
        # Add a horizontal box layout to put our plus and minus buttons side by side in
        self.add_sub_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(self.add_sub_layout)
        # Add our plus and minus buttons
        self.add_button = qt.PushButton(self.root,
                                        text='+',
                                        layout=self.add_sub_layout,
                                        func=self.add_row)
        self.subtract_button = qt.PushButton(self.root,
                                        text='-',
                                        layout=self.add_sub_layout,
                                        func=self.remove_row)
        # Add our back button and next button
        self.nav_btn_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(self.nav_btn_layout)
        self.back_button = qt.PushButton(self.root,
                                         text='Back',
                                         layout=self.nav_btn_layout,
                                         func=self.back_to_path_select)
        self.nav_btn_layout.addSpacing(100)
        self.next_button = qt.PushButton(self.root,
                                         text='Next',
                                         layout=self.nav_btn_layout,
                                         func=self.go_photo_select)
        self.show()

    @qt.QtCore.Slot()
    def add_row(self, *args, **kwargs):
        # This function pops when the + button is pressed
        # Add 1 to the row count
        self.row_count += 1
        # Add the LineEdit to the dictionary
        self.entry_rows.append(qt.LineEdit(self.root,
                                           placeholderText='Enter a name here',
                                           layout=self.line_layout))

    @qt.QtCore.Slot()
    def remove_row(self, *args, **kwargs):
        # This function pops when the - button is pressed
        # if the row count is 1, we return, thus ignoring the call to delete because there must be one row.
        if self.row_count == 1:
            return False
        # Make a variable to easily access the instance of the lineedit widget
        wid = self.entry_rows[-1]
        this_name = wid.text()
        # Remove the widget from the layout
        self.line_layout.removeWidget(wid)
        # Mark the widget for deletion
        wid.deleteLater()
        # Delete the line from the dictionary
        del self.entry_rows[-1]
        # remove the name from the names list, if it exists
        try:
            del self.root.names_list[self.root.names_list.index(this_name)]
        except ValueError:
            pass
        # Subtract 1 from the row count (new row count)
        self.row_count -= 1
        # Return true in case we ever need that functionality for some reason
        return True

    @qt.QtCore.Slot()
    def back_to_path_select(self, *args, **kwargs):
        self.load_page(self.root.path_entry_widget,
                       path_entry.PathEntryWidget)

    @qt.QtCore.Slot()
    def go_photo_select(self, *args, **kwargs):
        # This function pops when the Next button is pressed.
        # If the list is not blank:
        self.get_names()
        if self.root.names_list:
            self.load_page(self.root.photo_select_widget,
                           photo_select.PhotoSelectWidget)

    def get_names(self, *args, **kwargs):
        # reset the list to write in whatever is there now
        self.root.names_list = []
        # For every line in the list:
        for i in range(len(self.entry_rows)):
            # Name will be the text from the lineedit stripped of leading and trailing space
            name = self.entry_rows[i].text().strip()
            # If the name isn't blank, append it to the list
            if name:
                self.root.names_list.append(name)