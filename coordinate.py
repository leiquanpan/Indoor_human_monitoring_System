from PIL import Image
import face_recognition
import turtle

# Load the jpg file into a numpy array
image = face_recognition.load_image_file("received_picture_1522877227.6772435.jpeg")

# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py
face_locations = face_recognition.face_locations(image)

w, h = 3, 4;
Matrix = [[0 for x in range(w)] for y in range(h)] 

print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()
    mid_point_x=left+(right-left)/2 
    mid_point_y=top+(bottom-top)/2
    print("midpoint at {},{}".format(mid_point_x,mid_point_y))
    if mid_point_x>=442 and mid_point_x<=617 and mid_point_y>=541 and mid_point_y<=671:
    	Matrix[0][0]=1;
    	print("seat(0,0) occupied")
    if mid_point_x>=508 and mid_point_x<=693 and mid_point_y>=455 and mid_point_y<=538:
    	Matrix[1][0]=1;
    	print("seat(1,0) occupied")
    if mid_point_x>=584 and mid_point_x<=735 and mid_point_y>=428 and mid_point_y<=507:
    	Matrix[2][0]=1;
    	print("seat(2,0) occupied")
    if mid_point_x>=658 and mid_point_x<=816 and mid_point_y>=383 and mid_point_y<=464:
    	Matrix[3][0]=1;
    	print("seat(3,0) occupied")
    if mid_point_x>=998 and mid_point_x<=1212 and mid_point_y>=527 and mid_point_y<=669:
    	Matrix[0][1]=1;
    	print("seat(0,1) occupied")
    if mid_point_x>=992 and mid_point_x<=1184 and mid_point_y>=410 and mid_point_y<=521:
    	Matrix[1][1]=1;
    	print("seat(1,1) occupied")
    if mid_point_x>=1000 and mid_point_x<=1159 and mid_point_y>=455 and mid_point_y<=541:
    	Matrix[2][1]=1;
    	print("seat(2,1) occupied")
    if mid_point_x>=1013 and mid_point_x<=1149 and mid_point_y>=377 and mid_point_y<=450:
    	Matrix[3][1]=1;
    	print("seat(3,1) occupied")
    if mid_point_x>=1556 and mid_point_x<=1704 and mid_point_y>=522 and mid_point_y<=623:
    	Matrix[0][2]=1;
    	print("seat(0,2) occupied")
    if mid_point_x>=1432 and mid_point_x<=1584 and mid_point_y>=430 and mid_point_y<=522:
    	Matrix[1][2]=1;
    	print("seat(1,2) occupied")
    if mid_point_x>=1385 and mid_point_x<=1519 and mid_point_y>=422 and mid_point_y<=493:
    	Matrix[2][2]=1;
    	print("seat(2,2) occupied")
    if mid_point_x>=1318 and mid_point_x<=1459 and mid_point_y>=381 and mid_point_y<=449:
    	Matrix[3][2]=1;
    	print("seat(3,2) occupied")
    print(Matrix);
turtle.left(20)

turtle.forward(50)
turtle.left(90)
turtle.forward(50)
turtle.left(90)
turtle.forward(50)
turtle.left(90)
turtle.forward(50)
turtle.left(90)

