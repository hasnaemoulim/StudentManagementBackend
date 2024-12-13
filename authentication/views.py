from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser, IsEnseignantUser

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        print(f"User: {request.user}, Role: {request.user.role}")
        return Response({"message": "Bienvenue dans l'espace Admin !"})

class EnseignantOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsEnseignantUser]

    def get(self, request):
        print(f"User: {request.user}, Role: {request.user.role}")
        return Response({"message": "Bienvenue dans l'espace Enseignant !"})
