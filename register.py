import cv2
import face_recognition
import os
import pickle
import config

if not os.path.exists(config.DATA_DIR):
    os.makedirs(config.DATA_DIR)    

def updateData(name, values):
    data = {}
    
    if os.path.exists(config.DB_PATH):
        try:
            with open("faceData.pickle", "rb") as f:
                data = pickle.load(f)
        except:
            return False, 'File reading error.'
        
    if name in data:
        return 'Already exists.'

    try:
        data[name] = values
        with open(config.DB_PATH, "wb") as f:
            pickle.dump(data, f)
        return True, name + ' added.'
    except:
        return False, 'File writing error.'
    
def main():
    camera = cv2.VideoCapture(config.CAMERA_ID)

    if not camera.isOpened():
        return False, 'Camera error.'

    while True:
        ret, frame = camera.read()

        if not ret:
            break
        
        originalFrame = frame.copy()
        reducedFrame = cv2.resize(frame, (0,0), fx=config.SCALE_FACTOR, fy=config.SCALE_FACTOR)
        rgb_frame = cv2.cvtColor(reducedFrame, cv2.COLOR_BGR2RGB)
        
        faceLocation = face_recognition.face_locations(rgb_frame, model=config.MODEL)
        
        if len(faceLocation) == 1:
            text = "Press 's' to register."
            color = config.COLOR_GREEN

        elif len(faceLocation) == 0:
            text = "There is no face to register."
            color = config.COLOR_RED

        elif len(faceLocation) > 1:
            text = "There are too many faces."
            color = config.COLOR_RED
        
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.imshow("Register Mode", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        elif key == ord('s') and len(faceLocation) == 1:
            data = face_recognition.face_encodings(rgb_frame, faceLocation)
            
            if len(data) == 1:
                name = input("Name to register: ").strip().upper()

                if name:
                    updateData(name, data[0])
                    break
            
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()