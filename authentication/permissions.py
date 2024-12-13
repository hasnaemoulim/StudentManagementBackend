from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et si son rôle est "Admin"
        return request.user.is_authenticated and request.user.role == 'Admin'

class IsEnseignantUser(BasePermission):
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et si son rôle est "Enseignant"
        return request.user.is_authenticated and request.user.role == 'Enseignant'