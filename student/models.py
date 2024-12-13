from django.db import models
from django.db import models
from django.utils.timezone import now



STATUS_CHOICES = [
    ('Present', 'Present'),
    ('Absent', 'Absent'),
]

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)  # Identifiant unique
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    image = models.ImageField(upload_to='student_images/', null=True, blank=True)  # Nouveau champ image

    def __str__(self):
        return f"{self.student_id}: {self.first_name} {self.last_name}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Present')
    recorded_at = models.DateTimeField(auto_now_add=True)  # Nouveau champ pour la date et l'heure d'enregistrement

    def __str__(self):
        return f"{self.student.student_id} - {self.status} on {self.date}"
