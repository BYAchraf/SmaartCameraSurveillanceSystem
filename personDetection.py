import cv2
import time
import numpy as np
import face_recognition
from sendNotif import Notification

face_database=dict()
face_database_count=1
notification = Notification()

def saveFaces(frame, faces_locations, id):
    global notification
    for face in faces_locations:
        roiName = "face"+str(id)+".jpg"
        cv2.imwrite(roiName, frame[face[0]:face[2], face[3]:face[1]])
        frameName = "frame_"+roiName
        cv2.imwrite(frameName, frame)
        notification.sendNotification([roiName, frameName])

def add_face(frame, face, faces_locations):
    global face_database
    global face_database_count
    saveFaces(frame, faces_locations, face_database_count)
    face_database[face_database_count] = face
    face_database_count += 1

def getIdFace(frame, face_encoded, faces_locations):
    global face_database
    global face_database_count

    if face_database:
        existingFace = face_recognition.compare_faces([face for face in face_database.values()], face_encoded)
        if any(existingFace):
            return np.argmax(existingFace)+1
        else:
            add_face(frame, face_encoded, faces_locations)
            return face_database_count-1
    add_face(frame, face_encoded, faces_locations)
    return face_database_count-1


def detection():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        try:
            encoding = face_recognition.face_encodings(frame)[0]
            face_location = face_recognition.face_locations(frame)
            id = getIdFace(frame, encoding, face_location)
            print(id)
        except:
            pass
        cv2.imshow('SCSS', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def detectionFlask():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        try:
            encoding = face_recognition.face_encodings(frame)[0]
            face_location = face_recognition.face_locations(frame)
            id = getIdFace(frame, encoding, face_location)
        except:
            pass
        # frame = cv2.resize(frame, (0,0), fx=1.0, fy=1.0) 
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    detection()
