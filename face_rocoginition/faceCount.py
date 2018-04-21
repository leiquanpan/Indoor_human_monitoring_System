# This file is for recognizing human face in a given image
# There is two parameters
# -f filePath: image input path
# -e endPath: image output path


from PIL import Image
import face_recognition
import cv2
from datetime import datetime
import argparse

# For firebase sdk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import json

#Read commandline parameters
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filePath", action="store", required=True, dest="filePath", help="image file input path")
parser.add_argument("-e", "--endPath", action="store", required=True, dest="endPath", help="image file output path")

args = parser.parse_args()
filePath = args.filePath
endPath = args.endPath


# Load the jpg file into a numpy array
image = face_recognition.load_image_file(filePath)

#initialize matrix
w, h = 3, 4;
Matrix = [[0 for x in range(w)] for y in range(h)]

#get firebase reference
cred = credentials.Certificate('/home/ubuntu/json_file/bigbrother-187c7-firebase-adminsdk-kbahd-ca4e377409.json')

firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://bigbrother-187c7.firebaseio.com/',
    'storageBucket' : 'gs://bigbrother-187c7.appspot.com'
})

ref = db.reference('rooms/lopata302/distribution')


# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py
face_locations = face_recognition.face_locations(image)

# draw a rectangular on all the faces, and print their number
for face_location in face_locations:
    top, right, bottom, left = face_location
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(image, "FACE", (left + 6, bottom - 6), font, 1, (255, 255, 255), 1)
    
    mid_point_x=left+(right-left)/2
    mid_point_y=top+(bottom-top)/2

    if mid_point_x>=442 and mid_point_x<=617 and mid_point_y>=541 and mid_point_y<=671:
        Matrix[0][0]=1
        ref.update({
            'A0':True
        })
    else: 
        Matrix[0][0]=0
        ref.update({
            'A0':False
        })
    if mid_point_x>=508 and mid_point_x<=693 and mid_point_y>=455 and mid_point_y<=538:
        Matrix[1][0]=1
        ref.update({
            'B0':True
        })
    else: 
        Matrix[1][0]=0
        ref.update({
            'B0':False
        })
    if mid_point_x>=584 and mid_point_x<=735 and mid_point_y>=428 and mid_point_y<=507:
        Matrix[2][0]=1
        ref.update({
            'C0':True
        })
    else: 
        Matrix[2][0]=0
        ref.update({
            'C0':False
        })
    if mid_point_x>=658 and mid_point_x<=816 and mid_point_y>=383 and mid_point_y<=464:
        Matrix[3][0]=1
        ref.update({
            'D0':True
        })
    else: 
        Matrix[3][0]=0
        ref.update({
            'D0':False
        })
    if mid_point_x>=998 and mid_point_x<=1212 and mid_point_y>=527 and mid_point_y<=669:
        Matrix[0][1]=1
        ref.update({
            'A1':True
        })
    else: 
        Matrix[0][1]=0
        ref.update({
            'A1':False
        })
    if mid_point_x>=992 and mid_point_x<=1184 and mid_point_y>=410 and mid_point_y<=521:
        Matrix[1][1]=1
        ref.update({
            'B1':True
        })
    else: 
        Matrix[1][1]=0
        ref.update({
            'B1':False
        })
    if mid_point_x>=1000 and mid_point_x<=1159 and mid_point_y>=455 and mid_point_y<=541:
        Matrix[2][1]=1
        ref.update({
            'C1':True
        })
    else:
        Matrix[2][1]=0
        ref.update({
            'C1':False
        })
    if mid_point_x>=1013 and mid_point_x<=1149 and mid_point_y>=377 and mid_point_y<=450:
        Matrix[3][1]=1
        ref.update({
            'D1':True
        })
    else:
        Matrix[3][1]=0
        ref.update({
            'D1':False
        })
    if mid_point_x>=1556 and mid_point_x<=1704 and mid_point_y>=522 and mid_point_y<=623:
        Matrix[0][2]=1
        ref.update({
            'A2':True
        })
    else:
        Matrix[0][2]=0
        ref.update({
            'A2':False
        })
    if mid_point_x>=1432 and mid_point_x<=1584 and mid_point_y>=430 and mid_point_y<=522:
        Matrix[1][2]=1
        ref.update({
            'B2':True
        })
    else:
        Matrix[1][2]=0
        ref.update({
            'B2':False
        })
    if mid_point_x>=1385 and mid_point_x<=1519 and mid_point_y>=422 and mid_point_y<=493:
        Matrix[2][2]=1
        ref.update({
            'C2':True
        })
    else:
        Matrix[2][2]=0
        ref.update({
            'C2':False
        })
    if mid_point_x>=1318 and mid_point_x<=1459 and mid_point_y>=381 and mid_point_y<=449:
        Matrix[3][2]=1
        ref.update({
            'D2':True
        })
    else:
        Matrix[3][2]=0
        ref.update({
            'D2':False
        })

# get current distribution and write to a json file for web use
with open('matrix.json', 'w') as f:
    f.write(json.dumps(str(ref.get())))

#cv2.putText(frame, text, (), font, 1, (255, 255, 255), 1)
#store the photo in the endPath
time = str(datetime.now())
outputPath = endPath + "/processed_picture_" + time + ".jpg"
cv2.imwrite(outputPath,image)

#you need to put matrix into database.

