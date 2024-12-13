# face_detection_real_time.py
import cv2
import face_recognition
import numpy as np
import requests

# Charger les encodages des visages connus et leurs noms
known_face_encodings = []
known_face_names = []

image_dir = "media/student_images"  # Dossier contenant les images des étudiants

# Charger les images des étudiants et générer les encodages
import os
for file_name in os.listdir(image_dir):
    if file_name.endswith(('.jpg', '.jpeg', '.png')):  # Vérifier les extensions valides
        image_path = os.path.join(image_dir, file_name)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]  # Prend le premier encodage trouvé

        known_face_encodings.append(encoding)
        known_face_names.append(file_name.split(".")[0])  # Utilise le nom du fichier comme nom de l'étudiant

# Accéder à la caméra
video_capture = cv2.VideoCapture(0)

# Initialisation d'une liste pour éviter l'enregistrement multiple
attendance_recorded = set()

# URL de l'API Django pour enregistrer la présence
attendance_api_url = "http://127.0.0.1:8000/student/attendance/"  # Adapter si nécessaire

while True:
    # Lire l'image depuis la caméra
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]  # Convertir BGR en RGB (nécessaire pour face_recognition)

    # Détecter les visages et encoder leurs caractéristiques
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Comparer le visage détecté avec les visages connus
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Inconnu"

        # Trouver le visage connu le plus proche
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

            # Enregistrer la présence si ce n'est pas déjà fait
            if name not in attendance_recorded:
                student_id = name  # Supposons que le nom du fichier est l'ID étudiant
                response = requests.post(attendance_api_url, data={"student_id": student_id, "status": "Present"})
                if response.status_code == 201:
                    print(f"Présence enregistrée pour {student_id}")
                    attendance_recorded.add(name)  # Ajouter à la liste des étudiants enregistrés
                else:
                    print(f"Erreur lors de l'enregistrement pour {student_id}: {response.json()}")

        # Dessiner un rectangle autour du visage
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Afficher la vidéo avec les annotations
    cv2.imshow('Video', frame)

    # Quitter avec la touche "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
video_capture.release()
cv2.destroyAllWindows()
