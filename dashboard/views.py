from copyreg import constructor
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers


from .models import Attendance, StudentList


import pandas as pd
import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition


# Create your views here.


def dashboard(request):

    studs = StudentList.objects.all()
    return render(request, 'dashboard.html', {'studs': studs})


def runModel():
    Attendance.objects.all().delete()

    path = '/home/aboozuhaib/Documents/miniproject/Face-Recognition-esp32/student_images'
    url = 'http://192.168.1.39/cam-hi.jpg'


    images = []
    classNames = []
    rollNumbers = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        splitName = os.path.splitext(cl)[0]
        classNames.append(splitName)
        splitRoll = splitName.split("_")[1]
        rollNumbers.append(splitRoll)

    print('Encoding in Progress')

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    encodeListKnown = findEncodings(images)

    def addAttendence(name):

        if (Attendance.objects.filter(name = name).exists()):
            print('already exists')

        else:
            time = datetime.now().strftime('%H:%M:%S')
            a = Attendance(name=name, time=time)
            a.save()

    print('Encoding Complete')
    pre_name = 'testuser'

    while True:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = rollNumbers[matchIndex].upper()

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                              (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                if (pre_name != name):
                    pre_name = name
                    addAttendence(name)

        cv2.imshow('Webcam', img)
        key = cv2.waitKey(5)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    cv2.imread



def update(request):
    print(request.method)
    if request.method == 'POST':

        runModel()
        return JsonResponse({'ok': True})
    else:
        return HttpResponse("page not found")


def getAtt(request):
    print(request.method)
    if request.method == 'POST':
        att = serializers.serialize("json", Attendance.objects.all())
        data = {"attendance": att}
        return JsonResponse(data)
    else:
        return HttpResponse("page note found")

def dispList(request):
    if request.method == 'GET':
        stdlist = serializers.serialize("json", StudentList.objects.all())
        studs = {"studentlist": stdlist}
        return JsonResponse(studs)
    else:
        return HttpResponse("page note found")
