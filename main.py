import cv2
import face_recognition
import os
import json
import pickle
import numpy as np
import datetime
import config


class faceid:
    def __init__(self):
        self.uploadedFaces = []
        self.uploadedNames = []
        self.updateData()
        self.system_active = False
        self.authorized_user = None

    def updateData(self):
        if not os.path.exists(config.DB_PATH):
            return False, 'There is no face data.'

        try:
            with open(config.DB_PATH, "rb") as f:
                data = pickle.load(f)

            self.uploadedNames = list(data.keys())
            self.uploadedFaces = list(data.values())
            return True, 'Data uploaded.'

        except Exception as e:
            return False, e

    def updateStatus(self, name):
        attempt = {
            "system_active": True,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "authorized": True,
            "user_name": name,
            "status_message": f"Successed. {name}"
        }

        try:
            if os.path.exists(config.JSON_PATH):
                with open(config.JSON_PATH, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

            data.append(attempt)

            with open(config.JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True, "JSON updated."

        except Exception as e:
            return False, e
        
    def run(self):
        cap = cv2.VideoCapture(config.CAMERA_ID)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if not self.system_active:
                reducedFrame = cv2.resize(frame, (0, 0), fx=config.SCALE_FACTOR, fy=config.SCALE_FACTOR)
                rgb_frame = cv2.cvtColor(reducedFrame, cv2.COLOR_BGR2RGB)

                faceLocation = face_recognition.face_locations(rgb_frame, model=config.MODEL)

                if len(faceLocation) == 1:
                    faceData = face_recognition.face_encodings(rgb_frame, faceLocation)

                    if len(faceData) == 1:
                        currentData = faceData[0]

                        comparedValues = face_recognition.compare_faces(self.uploadedFaces, currentData, tolerance=config.TOLERANCE)
                        distanceResults = face_recognition.face_distance(self.uploadedFaces, currentData)

                        if len(distanceResults) > 0:
                            bestMatch = np.argmin(distanceResults)

                            if comparedValues[bestMatch]:
                                self.system_active = True
                                self.authorized_user = self.uploadedNames[bestMatch]

                                self.updateStatus(self.authorized_user)

            if self.system_active:
                color = config.COLOR_GREEN
                text = f"System Unlocked. Welcome {self.authorized_user}"
            else:
                color = config.COLOR_RED
                text = "System Locked."

            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1)
            cv2.imshow("FaceID Matrix Mode", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = faceid()
    app.run()
