from django.urls import path
from .views import StudentListCreateView, StudentDetailView,AttendanceRecordView
from django.urls import path
from .views import FaceRecognitionAttendanceView




urlpatterns = [
    path('', StudentListCreateView.as_view(), name='student_list_create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('attendance/', AttendanceRecordView.as_view(), name='attendance_record'),

    path('face-recognition/', FaceRecognitionAttendanceView.as_view(), name='face_recognition'),



]
