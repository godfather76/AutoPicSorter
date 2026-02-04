# from mtcnn.mtcnn import MTCNN
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
from os import path, walk
from PIL import Image, ImageOps
from deepface import DeepFace

# May not need these
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.layers import Flatten, Dense, Resizing
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from keras_vggface import VGGFace
from collections import Counter

face_threshold = 0.97
num_pics_per_person = 10
prediction_threshold = 0.97


# def get_face(image, face):
#     x1, y1, w, h = face['box']
#
#     if w > h:
#         x1 = x1 + ((w - h) // 2)
#         w = h
#     elif h > w:
#         y1 = y1 + ((h - w) // 2)
#         h = w
#
#     x2 = x1 + h
#     y2 = y1 + w
#
#     return image[y1:y2, x1:x2]


# def label_faces(path, model, names, face_threshold=face_threshold,
#                 prediction_threshold=prediction_threshold,
#                 show_outline=True, size=(12, 8)):
#     # Load the image and orient it correctly
#     pil_image = Image.open(path)
#     exif = pil_image.getexif()
#
#     for k in exif.keys():
#         if k != 0x0112:
#             exif[k] = None
#             del exif[k]
#
#     pil_image.info["exif"] = exif.tobytes()
#     pil_image = ImageOps.exif_transpose(pil_image)
#     np_image = np.array(pil_image)
#
#     # fig, ax = plt.subplots(figsize=size, subplot_kw={'xticks': [], 'yticks': []})
#     # ax.imshow(np_image)
#
#     detector = MTCNN()
#     faces = detector.detect_faces(np_image)
#     faces = [face for face in faces if face['confidence'] > face_threshold]
#
#     face_list = []
#     for face in faces:
#         x, y, w, h = face['box']
#
#         # Use the model to identify the face
#         face_image = get_face(np_image, face)
#         face_image = image.array_to_img(face_image)
#         face_image = preprocess_input(np.array(face_image))
#         predictions = model.predict(np.expand_dims(face_image, axis=0))
#         # print(path)
#         # print(predictions)
#         confidence = np.max(predictions)
#         index = int(np.argmax(predictions))
#         # if confidence > prediction_threshold:
#         face_list.append(names[index])
#     face_list.sort()
#     return face_list




# def load_imgs(path, label):
#     images = []
#     labels = []
#
#     # loop through the files in the path
#     for file in os.listdir(path):
#         # load the image
#         img = image.load_img(os.path.join(path, file), target_size=(224, 224, 3))
#         # This flips the image right side up if it was flipped in phone's metadata
#         img = ImageOps.exif_transpose(img)
#         # make the image into an array and append it to our list of image arrays
#         images.append(image.img_to_array(img))
#         # append the label to our labels
#         labels.append((label))
#
#     return images, labels


def main(p, samples):
    train_sets_path = path.join(p, 'train_sets')
    main_dict = {}
    for root, dirs, files in walk(train_sets_path):
        main_dict = {x: [] for x in dirs}
        break

    for person in main_dict.keys():
        this_path = path.join(train_sets_path, person)
        for root, dirs, files in walk(this_path):
            for img_f in files:
                res_df = search_img(path.join(root, img_f))
                main_dict[person] += list(res_df['identity'])
            break
    main_dict = {x: set(y) for x, y in main_dict.items()}
    print(main_dict)

def search_img(img_f):
    pil_image = Image.open(img_f)
    fig, ax = plt.subplots()

    exif = pil_image.getexif()

    for k in exif.keys():
        if k != 0x0112:
            exif[k] = None
            del exif[k]
    pil_image.info["exif"] = exif.tobytes()
    pil_image = ImageOps.exif_transpose(pil_image)
    res_df = DeepFace.find(img_path=img_f,
                           db_path='/home/ike/Pictures/PicSorter/sample_pics',
                           enforce_detection=False)[0]

    return res_df


# def main_old(p, samples):
#     train_sets_path = os.path.join(p, 'train_sets')
#     x, y = [], []
#     people = []
#     for root, dirs, files in os.walk(train_sets_path):
#         people = dirs.copy()
#         for i, person in enumerate(people):
#             images, labels = load_imgs(os.path.join(root, person), i)
#             x += images
#             y += labels
#             # show_images(images)
#         break
#
#     faces = preprocess_input(np.array(x))
#     labels = np.array(y)
#
#     x_train, x_test, y_train, y_test = train_test_split(faces, labels,
#                                                         train_size=.6, stratify=labels,
#                                                         random_state=0)
#
#     # base_model = load_model('vggface.h5')
#     base_model = VGGFace()
#     base_model.trainable = False
#     model = Sequential()
#     model.add(Resizing(224, 224))
#     model.add(base_model)
#     model.add(Flatten())
#     model.add(Dense(8, activation='relu'))
#     model.add(Dense(len(people), activation='softmax'))
#     model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#
#
#
#     hist = model.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=2, epochs=10)
#
#     predicted_faces = {}
#     for sample in samples:
#         # use our model to label the faces in each photo
#         # the resulting dict is {path: [list of people in the photo]}
#         face_list = label_faces(sample, model, people)
#         predicted_faces[sample] = face_list
#
#     correct = 0
#     wrong = 0
#     total = 0
#     for p, pred in predicted_faces.items():
#         names_split = os.path.splitext(os.path.split(p)[1])[0].split('-')
#         del names_split[-1]
#         names = [x for x in names_split if x in people]
#         if Counter(names) == Counter(pred):
#             print(f'{p} was predicted successfully: {str(names)}')
#             correct += 1
#         else:
#             print(f'{p} predicted {str(pred)} but photo has {str(names)}')
#             wrong += 1
#         total += 1
#     print('Correct:', correct)
#     print('Wrong:', wrong)
#     print('Percent correct:', str((correct / total) * 100) + '%')

