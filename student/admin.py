from django.contrib import admin
from .models import Student, Attendance  # Importez les modèles nécessaires
from django.utils.html import format_html

# Enregistrement du modèle Student dans l'admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ('student_id', 'first_name', 'last_name', 'birth_date', 'status', 'image_preview')
    search_fields = ('student_id', 'first_name', 'last_name')

    # Affichage d'un aperçu de l'image
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'date_created')  # Remplacer recorded_at par date_created
    search_fields = ('student__student_id', 'student__first_name', 'student__last_name')
    list_filter = ('status', 'date')

    # Méthode pour afficher une date créée formatée
    def date_created(self, obj):
        return obj.date.strftime("%Y-%m-%d")
    date_created.short_description = 'Date Created'