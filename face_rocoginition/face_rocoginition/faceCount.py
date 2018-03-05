# This file is for recognizing human face in a given image
# There is two parameters
# -f filePath: image input path
# -e endPath: image output path


from PIL import Image
import face_recognition
import cv2
from datetime import datetime
import argparse
import time

#Read commandline parameters
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filePath", action="store", required=True, dest="filePath", help="image file input path")
parser.add_argument("-e", "--endPath", action="store", required=True, dest="endPath", help="image file output path")

args = parser.parse_args()
filePath = args.filePath
endPath = args.endPath


# Load the jpg file into a numpy array
image = face_recognition.load_image_file(filePath)

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
text = "There is " + str(len(face_locations)) + " human faces"

#cv2.putText(frame, text, (), font, 1, (255, 255, 255), 1)
#store the photo in the endPath
timestamp = str(time.time())
outputPath = endPath + "/processed_picture_" + timestamp + ".jpg"
cv2.imwrite(outputPath,image)

print("There is {} face(s).".format(len(face_locations)))

