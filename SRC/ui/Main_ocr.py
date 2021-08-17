import easyocr
import numpy as np
import os
import cv2 
import  pyscreenshot as ImageGrab
#from PIL import Image, ImageGrab, ImageFont, ImageDraw
import face_recognition
from datetime import datetime
import pprint
import time
#from views import frame 

start_time = datetime.now()
ts = time.gmtime()
ts = time.strftime("%Y-%m-%d %H:%M:%S", ts)
WINDOW_NAME = "Webcam"
def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened
name_to_write = "lisense"
def captureScreen(bbox=(-1400,0,790,900)): #bbox=(-1400,0,790,900)
    capScr = np.array(ImageGrab.grab(bbox))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr

photo_image = cv2.imread(r"/home/deepika/Desktop/ocr/MASTER/UIV2-master/ui/ID.jpg")
photo_size = photo_image.shape
photo_y1 = int(photo_size[0])
photo_height_top = round(0.294*photo_y1)
photo_y2 = int(photo_size[0])
photo_height_bottom = round(0.88*photo_y2)
photo_x1 = int(photo_size[1])
photo_width_left = round(0.702*photo_x1)
photo_x2 = int(photo_size[1])
photo_width_right = round(0.999*photo_x2)
# # print(photo_height_top,photo_height_bottom, photo_width_left,photo_width_right)
photo = photo_image[photo_height_top:photo_height_bottom, photo_width_left:photo_width_right]
print("photo----------------",photo)

reader = easyocr.Reader(['en','ja'])# need to run only once to load model into memory
name_size = photo_image.shape
name_y1 = int(name_size[0])
name_height_top = round(0*name_y1)
name_y2 = int(name_size[0])
name_height_bottom = round(0.087*name_y2)
name_x1 = int(name_size[1])
name_width_left = round(0.08*name_x1)
name_x2 = int(name_size[1])
name_width_right = round(0.62*name_x2)
name_result = photo_image[name_height_top:name_height_bottom, name_width_left:name_width_right]
#resized_name_image = re_size(name_result, 50, 50)
name_sharpened = unsharp_mask(photo_image)
name = reader.readtext(name_sharpened, detail=0, decoder = 'beamsearch', beamWidth= 10, batch_size = 5,\
                 workers = 0, allowlist = None, blocklist = None,\
                 rotation_info = None, paragraph = False, min_size = 20,\
                 contrast_ths = 0.4,adjust_contrast = 0.5,\
                 text_threshold = 0.8, low_text = 0.4, link_threshold = 0.9,\
                 canvas_size = 2560, mag_ratio = 1.,\
                 slope_ths = 0.1, ycenter_ths = 0.5, height_ths = 0.5,\
                 width_ths = 0.5, y_ths = 0.5, x_ths = 1.0, add_margin = 0.1)

# cv2.waitKey(0)
path = r'/image'
#cv2.imshow("photo", photo)
cv2.waitKey(0)
print(name)

os.chdir("/home/deepika/Desktop/ocr/MASTER/UIV2-master/ui/ui/static")
photo = cv2.imwrite("lisense.jpg",photo)
#cv2.imshow("photo", photo)
#cv2.imwrite(os.path.join(path, name_to_write + ".jpg"), photo)
path = '/home/deepika/Desktop/ocr/MASTER/UIV2-master/ui/ui'
images = []
classNames = []
myList = os.listdir(path)
name_write="lisense"
print("myList---------------------------------------------",os.listdir(path)) 
#  file_first_name i am supposed to search for test_5 file while keeping the name from not ocr output  name_write
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(name_write)[0])
#print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

