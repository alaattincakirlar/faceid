import cv2
import face_recognition
import os
import numpy as np

uploaded_faceData = []
uploaded_faceNames = []

images = os.listdir('data')

for image in images:
    if image.endswith('.jpg'):
        data = face_recognition.face_encodings(face_recognition.load_image_file('data/' + image))
        
        if len(data) > 0:
            uploaded_faceData.append(data[0])
            uploaded_faceNames.append(os.path.splitext(image)[0])

camera = cv2.VideoCapture(0)

flag = 0

while True:
    ret, frame = camera.read()
    if not ret:
        break

    reducedFrame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)
    rgb_reducedFrame = cv2.cvtColor(reducedFrame, cv2.COLOR_BGR2RGB)

    faceLocation = face_recognition.face_locations(rgb_reducedFrame)
    faceData = face_recognition.face_encodings(rgb_reducedFrame, faceLocation)
    verification = 'not done'

    for face_encoding, face_loc in zip(faceData, faceLocation):
        compareValues = face_recognition.compare_faces(uploaded_faceData, face_encoding, tolerance=0.6)
        distanceValues = face_recognition.face_distance(uploaded_faceData, face_encoding)
                
        if len(distanceValues) > 0:
            bestMatch = np.argmin(distanceValues)
            
            if compareValues[bestMatch]:
                name = uploaded_faceNames[bestMatch]
                color = (0, 255, 0)
                status = 'Verification is done.\nWelcome ' + name
                verification = 'done'

            else:
                name = 'Unknown.'
                color = (0, 0, 255)
                status = 'Verification denied.'
    
    if verification == 'done' or flag == 1:
        cv2.putText(frame, 'Verification is done. Welcome ' + name, (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 1)
        flag = 1

    else:
        cv2.putText(frame, 'Verification denied.', (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 1)


    cv2.imshow('FaceID Verification', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()