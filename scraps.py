from mtcnn.mtcnn import MTCNN
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image, ImageOps
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.layers import Flatten, Dense, Resizing
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model, Sequential

face_threshold = 0.95
num_pics_per_person = 10
prediction_threshold = 0.95


def get_face(image, face):
    x1, y1, w, h = face['box']

    if w > h:
        x1 = x1 + ((w - h) // 2)
        w = h
    elif h > w:
        y1 = y1 + ((h - w) // 2)
        h = w

    x2 = x1 + h
    y2 = y1 + w

    return image[y1:y2, x1:x2]


def label_faces(path, model, names, face_threshold=face_threshold,
                prediction_threshold=prediction_threshold,
                show_outline=True, size=(12, 8)):
    # Load the image and orient it correctly
    pil_image = Image.open(path)
    exif = pil_image.getexif()

    for k in exif.keys():
        if k != 0x0112:
            exif[k] = None
            del exif[k]

    pil_image.info["exif"] = exif.tobytes()
    pil_image = ImageOps.exif_transpose(pil_image)
    np_image = np.array(pil_image)

    fig, ax = plt.subplots(figsize=size, subplot_kw={'xticks': [], 'yticks': []})
    ax.imshow(np_image)

    detector = MTCNN()
    faces = detector.detect_faces(np_image)
    faces = [face for face in faces if face['confidence'] > face_threshold]

    face_list = []
    for face in faces:
        x, y, w, h = face['box']

        # Use the model to identify the face
        face_image = get_face(np_image, face)
        face_image = image.array_to_img(face_image)
        face_image = preprocess_input(np.array(face_image))
        predictions = model.predict(np.expand_dims(face_image, axis=0))
        confidence = np.max(predictions)
        index = int(np.argmax(predictions))
        if confidence > prediction_threshold:
            face_list.append(names[index])
    face_list.sort()
    return face_list




def load_imgs(path, label):
    images = []
    labels = []

    # loop through the files in the path
    for file in os.listdir(path):
        # load the image
        img = image.load_img(os.path.join(path, file), target_size=(224, 224, 3))
        # This flips the image right side up if it was flipped in phone's metadata
        img = ImageOps.exif_transpose(img)
        # make the image into an array and append it to our list of image arrays
        images.append(image.img_to_array(img))
        # append the label to our labels
        labels.append((label))

    return images, labels


def main():
    p = '/home/isaac/Pictures/'
    train_samples_path = os.path.join(p, 'training_samples')
    x, y = [], []
    people = []
    for root, dirs, files in os.walk(train_samples_path):
        people = dirs.copy()
        for i, person in enumerate(people):
            images, labels = load_imgs(os.path.join(root, person), i)
            x += images
            y += labels
            # show_images(images)
        break

    faces = preprocess_input(np.array(x))
    labels = np.array(y)

    x_train, x_test, y_train, y_test = train_test_split(faces, labels,
                                                        train_size=.6, stratify=labels,
                                                        random_state=0)

    base_model = load_model('vggface.h5')
    base_model.trainable = False

    model = Sequential()
    model.add(Resizing(224, 224))
    model.add(base_model)
    model.add(Flatten())
    model.add(Dense(8, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    hist = model.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=2, epochs=10)

    predicted_faces = {}
    for root, dirs, files in os.walk(os.path.join(p, 'test_pics')):
        for file in files:
            # use our model to label the faces in each photo
            # the resulting dict is {path: [list of people in the photo]}
            face_list = label_faces(os.path.join(root, file), model, people)
            predicted_faces[file] = face_list
        break
    print(predicted_faces)

class CustomTitleBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None
        title_bar_layout = QtWidgets.QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)
        self.title = QtWidgets.QLabel(f"{self.__class__.__name__}", self)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(
            """
        QLabel { text-transform: uppercase; font-size: 10pt; margin-left: 48px; }
        """
        )

        if title := parent.windowTitle():
            self.title.setText(title)
        title_bar_layout.addWidget(self.title)
        # Min button
        self.min_button = QtWidgets.QToolButton(self)
        min_icon = QtGui.QIcon()
        min_icon.addFile("min.svg")
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QtWidgets.QToolButton(self)
        max_icon = QtGui.QIcon()
        max_icon.addFile("max.svg")
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QtWidgets.QToolButton(self)
        close_icon = QtGui.QIcon()
        close_icon.addFile("close.svg")  # Close has only a single state.
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QtWidgets.QToolButton(self)
        normal_icon = QtGui.QIcon()
        normal_icon.addFile("normal.svg")
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        # Add buttons
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QtCore.QSize(16, 16))
            button.setStyleSheet(
                """QToolButton {
                    border: none;
                    padding: 2px;
                }
                """
            )
            title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        if state == QtCore.Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)
