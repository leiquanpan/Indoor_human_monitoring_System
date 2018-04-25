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

   
    if mid_point_x>=294 and mid_point_x<=496 and mid_point_y>=459 and mid_point_y<=588:
        Matrix[0][0]=1
        ref.update({
            'A0':True
        })
    if mid_point_x>=437 and mid_point_x<=566 and mid_point_y>=369 and mid_point_y<=450:    
        Matrix[1][0]=1
        ref.update({
            'B0':True
        })
    if mid_point_x>=579 and mid_point_x<=685 and mid_point_y>=354 and mid_point_y<=437:    
        Matrix[2][0]=1
        ref.update({
            'C0':True
        })
    if mid_point_x>=657 and mid_point_x<=785 and mid_point_y>=331 and mid_point_y<=425:    
        Matrix[3][0]=1
        ref.update({
            'D0':True
        })
    if mid_point_x>=879 and mid_point_x<=1071 and mid_point_y>=484 and mid_point_y<=594:    
        Matrix[0][1]=1
        ref.update({
            'A1':True
        })
    if mid_point_x>=882 and mid_point_x<=1002 and mid_point_y>=386 and mid_point_y<=468:    
        Matrix[1][1]=1
        ref.update({
            'B1':True
        })
    if mid_point_x>=986 and mid_point_x<=1101 and mid_point_y>=367 and mid_point_y<=474:    
        Matrix[2][1]=1
        ref.update({
            'C1':True
        })
    if mid_point_x>=1007 and mid_point_x<=1113 and mid_point_y>=336 and mid_point_y<=428:    
        Matrix[3][1]=1
        ref.update({
            'D1':True
        })
    if mid_point_x>=1484 and mid_point_x<=1672 and mid_point_y>=514 and mid_point_y<=627:    
        Matrix[0][2]=1
        ref.update({
            'A2':True
        })
    if mid_point_x>=1393 and mid_point_x<=1584 and mid_point_y>=471 and mid_point_y<=579:    
        Matrix[1][2]=1
        ref.update({
            'B2':True
        })
    if mid_point_x>=1370 and mid_point_x<=1477 and mid_point_y>=357 and mid_point_y<=455:    
        Matrix[2][2]=1
        ref.update({
            'C2':True
        })
    if mid_point_x>=1254 and mid_point_x<=1381 and mid_point_y>=351 and mid_point_y<=442:    
        Matrix[3][2]=1
        ref.update({
            'D2':True
        })

# get current distribution and write to a json file for web use
with open('matrix.json', 'w') as f:
    f.write(json.dumps(ref.get()))

# reinitiate the firebase
ref.update({
     'A0':False,
     'A1':False,
     'A2':False,
     'B0':False,
     'B1':False,
     'B2':False,
     'C0':False,
     'C1':False,
     'C2':False,
     'D0':False,
     'D1':False,
     'D2':False
})
#cv2.putText(frame, text, (), font, 1, (255, 255, 255), 1)
#store the photo in the endPath
time = str(datetime.now())
outputPath = endPath + "/processed_picture_" + time + ".jpg"
cv2.imwrite(outputPath,image)

#you need to put matrix into database.

