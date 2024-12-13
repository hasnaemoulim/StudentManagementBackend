from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student,Attendance
from .serializers import StudentSerializer
from authentication.permissions import IsAdminUser  # Utilise la permission d'admin
from rest_framework.permissions import IsAuthenticated
import os
import cv2
import face_recognition
import torch
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Attendance


from django.http import JsonResponse
from rest_framework.views import APIView
import face_recognition
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from django.shortcuts import render


class StudentListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Étudiant introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({"error": "Étudiant introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"error": "Étudiant introuvable"}, status=status.HTTP_404_NOT_FOUND)


class AttendanceRecordView(APIView):
    def post(self, request):
        student_id = request.data.get("student_id")
        status_value = request.data.get("status", "Present")
        
        try:
            student = Student.objects.get(student_id=student_id)
            Attendance.objects.create(student=student, status=status_value)
            return Response({"message": "Attendance recorded successfully"}, status=status.HTTP_201_CREATED)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        

class FaceRecognitionAttendanceView(APIView):
    def get(self, request):
        # Charger les encodages des visages connus et leurs identités
        known_encodings = []
        known_student_ids = []
        student_images_dir = "media/student_images"

        for file_name in os.listdir(student_images_dir):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                # Extraire le nom sans l'extension
                base_name = os.path.splitext(file_name)[0]
                # Identifier l'ID de l'étudiant (supposons que c'est la première partie avant le caractère '_')
                student_id = base_name.split('_')[0]

                # Charger et encoder l'image
                image_path = os.path.join(student_images_dir, file_name)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_student_ids.append(student_id)

        # Charger le modèle YOLO pour la détection des visages
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        # Initialiser la capture vidéo
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Utiliser YOLO pour détecter les visages dans le cadre
            results = model(frame)
            detections = results.xyxy[0]  # Récupérer les détections sous forme de tableau

            for detection in detections:
                # Extraire les coordonnées de la boîte englobante
                x1, y1, x2, y2, conf, cls = map(int, detection[:6])

                # Recadrer la région d'intérêt (ROI)
                face_roi = frame[y1:y2, x1:x2]
                rgb_face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)

                # Reconnaissance faciale avec face_recognition
                face_encodings = face_recognition.face_encodings(rgb_face_roi)
                if face_encodings:
                    face_encoding = face_encodings[0]
                    matches = face_recognition.compare_faces(known_encodings, face_encoding)
                    name = "Inconnu"

                    if True in matches:
                        match_index = matches.index(True)
                        student_id = known_student_ids[match_index]

                        # Marquer l'étudiant comme "Présent" dans la base de données
                        try:
                            student = Student.objects.get(student_id=student_id)
                            Attendance.objects.create(student=student, status="Present")
                            name = f"{student.first_name} {student.last_name}"
                        except Student.DoesNotExist:
                            name = "Non enregistré"

                    # Dessiner un rectangle autour du visage et afficher le nom
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Afficher l'image
            cv2.imshow('Reconnaissance Faciale - Présence', frame)

            # Quitter avec la touche 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return JsonResponse({"message": "Processus de reconnaissance faciale terminé."})
