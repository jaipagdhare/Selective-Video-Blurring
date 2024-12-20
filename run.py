import cv2
import face_recognition
import os

def mosaic(image, x, y, w, h, blur_level=95):
    if w > 0 and h > 0:
        roi = image[y:y+h, x:x+w]
        if roi.size != 0:
            blurred_roi = cv2.GaussianBlur(roi, (blur_level, blur_level), 0)
            image[y:y+h, x:x+w] = blurred_roi
    return image

# faces = []
# for name in os.listdir("faces"):
#     if name.endswith(".png"):
#         image_path = os.path.join("faces", name)
#         image = face_recognition.load_image_file(image_path)
#         encodings = face_recognition.face_encodings(image)
        
#         if encodings:  # Check if encodings list is not empty
#             encoding = encodings[0]
#             faces.append(encoding)
#             print(image_path, encoding)
#         else:
#             print(f"No faces found in {image_path}")

input_video = cv2.VideoCapture('try.mp4')
if not input_video.isOpened():
  raise ValueError("Error opening video stream or file.")
else:
    print('parsing video')

output = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'),  30, (1080, 1920)) 

# length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
# width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = int(input_video.get(cv2.CAP_PROP_FPS))

# # Initialize the video writer for the output video
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# output_video = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

count = 0
while True:
    ret, frame = input_video.read()
    if not ret:
        break
    count += 1
    print('frame: ',count)
    location  = face_recognition.face_locations(frame,model='cnn')
    encodings = face_recognition.face_encodings(frame,location)

    for face_encodings,face_locations in zip(encodings,location):
        # results = face_recognition.compare_faces(faces,face_encodings,tolerance=0.5)
        top_left = (face_locations[3],face_locations[0])
        bottom_right = (face_locations[1],face_locations[2])
        cv2.rectangle(frame,top_left,bottom_right,(255,0,0),3)

    # output_video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    # cv2.imshow("",frame)
    output.write(frame) 
    if cv2.waitKey(5) & 0xFF == ord('q'): 
        break

    cv2.destroyAllWindows() 
    output.release() 
    input_video.release() 