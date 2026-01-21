import cv2
import os
import face_recognition

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    frameOriginal = frame.copy()
    if not ret:
        break

    rgb_reducedFrame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (0, 0), fx=0.25, fy=0.25)
    faces = face_recognition.face_locations(rgb_reducedFrame)

    if len(faces) == 0:
        status = 'There is no face to detect.'
        color = (0, 0, 255)

    elif len(faces) > 1:
        status = 'There are too many faces.'
        color = (0, 0, 255)

    else:
        status = 'Press S to register this face.'
        color = (0, 255, 0)


    cv2.putText(frame, status, (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.6, color, 1)
    cv2.imshow('Register Screen', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('s') and len(faces) == 1:
        name = str(input('Name to register: '))

        if not os.path.exists('data'):
                os.makedirs('data')

        cv2.imwrite('data/' + name + '.jpg', frameOriginal)
        print("Face registered as:", name)
        break

camera.release()
cv2.destroyAllWindows()