import PIL
from PIL import Image
from PIL.ExifTags import TAGS
from os import walk, path, mkdir, rename
from datetime import datetime
import binascii


def main():
    sorted_path = 'D:\\Pictures_sorted\\'
    for dirpath, dirs, files in walk(sorted_path):
        for fname in files:
            if dirpath != 'D:\\Pictures_sorted\\PossibleDuplicates':
                f_path = path.join(dirpath, fname)
                # if path.splitext(fname)[1].lower() == '.jpg' or path.splitext(fname)[1].lower() == '.jpeg':
                f_path = path.join(dirpath, fname)
                year_path = None
                day = None
                this_dt = None
                try:
                    image = Image.open(f_path)
                    exifdata = image.getexif()
                    for tagid in exifdata:
                        tagname = TAGS.get(tagid, tagid)
                        value = exifdata.get(tagid)
                        if fname == '06-09-2015 200630.JPG':
                            print(tagname, value)
                except PIL.UnidentifiedImageError:
                    pass
