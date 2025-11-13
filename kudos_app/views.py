from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Kudo
from .serializers import UserSerializer, KudosSerializer, KudoCreateSerializer
from datetime import timedelta
from django.utils import timezone

def kudosGiven(user):
    weekStart = timezone.now() - timedelta(days=timezone.now().weekday())
    return Kudo.objects.filter(sender=user, created_at__gte=weekStart).count()

# ---- All Users---
class AllUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
 
# --- Login ---
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username, password=password).first()
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ---- Users of Same Organization ----
class UserListView(APIView):
    def get(self, request, user_id):
        currUser = get_object_or_404(User, id=user_id)
        colleagues = User.objects.filter(organization = currUser.organization).exclude(id=currUser.id)
        serializer = UserSerializer(colleagues, many=True)
        return Response(serializer.data)
    
# --- Give Kudo ---    
class GiveKudoView(APIView):
    def post(self, request, sender_id):
        sender = get_object_or_404(User, id=sender_id)
        receiver_id = request.data.get('receiver_id')
        message = request.data.get('message')

        if not receiver_id:
            return Response({'error': 'Receiver ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        receiver = get_object_or_404(User, id=receiver_id)

        if sender == receiver:
            return Response({"error": "You cannot give kudos to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if sender.kudos_left <= 0:
            return Response({'error': f'{sender.username} has no kudos to give.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            kudo = Kudo.objects.create(sender=sender, receiver=receiver, message=message)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = KudosSerializer(kudo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# --- Received Kudos ---
class KudosReceivedView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        kudos = Kudo.objects.filter(receiver=user).order_by('-created_at')
        serializer = KudosSerializer(kudos, many=True)
        return Response(serializer.data)
    
# --- Rem Kudos ---
class RemainingKudosView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        # remaining = max(0,3 - kudosGiven(user))
        return Response({"remaining_kudos": user.kudos_left})