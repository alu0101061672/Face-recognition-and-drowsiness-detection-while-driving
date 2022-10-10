import requests
import cv2
import face_recognition
import numpy as np
import sys
from tkinter import *
from tkinter import messagebox
# #Implementar BD interna del vehículo para almacenar los datos del conductor. Por ahora se pasan por línea de comandos.

full_name = ""

for i in range(2, len(sys.argv)):
    full_name = full_name + sys.argv[i] + " "

digital_key ={
    "full_name": full_name[:-1],
    "dni": sys.argv[1]
}

print(digital_key)

# digital_key ={
#     "full_name": "Alba Cruz Torres",
#     "dni": "00000000L"
# }

response = requests.get("http://api-core:80/drivers/encoding/%s" % digital_key["dni"])
#response = requests.get("http://0.0.0.0:8000/drivers/encoding/%s" % digital_key["dni"])
encoding = response.json()
facial_embedding = np.array(encoding)
digital_key["facial_embedding"] = facial_embedding
print("Nombre completo: ", digital_key["full_name"], "\nDNI: ", digital_key["dni"], "\nEmbedding: ", digital_key["facial_embedding"], "\n")

cap = cv2.VideoCapture(0)

cont = 1000;
faceDistances = []

while cont >= 1:
    success, img = cap.read()
    resImg = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    resImg = cv2.cvtColor(resImg, cv2.COLOR_BGR2RGB)

    facesCurrFrame = face_recognition.face_locations(resImg)
    encodesCurrFrame = face_recognition.face_encodings(resImg, facesCurrFrame)

    for encodeFace, faceLoc in zip(encodesCurrFrame, facesCurrFrame):
        matches = face_recognition.compare_faces([facial_embedding], encodeFace)
        faceDistance = face_recognition.face_distance([facial_embedding], encodeFace)
        ##Mientras sea menor o igual que 0.6 se tratará de la misma persona.
        faceDistances.append(faceDistance)
        print(faceDistance)
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            name = digital_key["full_name"].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x1, y2, x2 = y1 * 4, x1 * 4, y2 * 4, x2 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2),(0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow('Webcam', img)
    cont = cont - 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Close the window 
cap.release() 
  
# De-allocate any associated memory usage 
cv2.destroyAllWindows()

status = False

for i in faceDistances:
    for x in i:
        if x <= 0.6:
            status = True
print(status)

if status:
    print("Puede arrancarrrr !")
    B1 = Button(text = "Success!", command = messagebox.showinfo("Success", "Face recognition correct. Engine can be started"))
    B1.place(x = 60, y = 60)
else:
    print(" No puede arrancar !")
    B1 = Button(text = "Error!", command = messagebox.showinfo("Error", "Face recognition incorrect. Engine cannot be started"))
    B1.place(x = 60, y = 60)