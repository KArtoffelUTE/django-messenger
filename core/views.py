from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

class MessageViewset(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        conversation = Conversation.objects.get(id=conversation_id)

        # User darf nur schreiben, wenn er Teilnehmer ist
        if not ConversationParticipant.objects.filter(conversation=conversation, user=self.request.user).exists():
            raise PermissionDenied("You are not a participant of this conversation.")

        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )

    def get_queryset(self):
        user = self.request.user
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(
            models.Q(conversation_id=conversation_id),
            models.Q(sender=user) | models.Q(conversation__participants__user=user)
        ).distinct().order_by('-timestamp')


class ConversationViewset(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        participants = serializer.validated_data.pop("participants")
        creator = self.request.user

        # Creator immer hinzufügen
        if creator.id not in participants:
            participants.append(creator.id)

        # DIRECT CHAT ERKENNUNG
        if len(participants) == 2:
            existing = (
                Conversation.objects
                .annotate(num_participants=models.Count("participants"))
                .filter(num_participants=2, participants__user__id__in=participants)
                .distinct()
            )

            # Prüfen, ob exakt diese zwei User drin sind
            for convo in existing:
                ids = list(convo.participants.values_list("user_id", flat=True))
                if sorted(ids) == sorted(participants):
                    # Conversation existiert → zurückgeben
                    self.existing_conversation = convo
                    return
        # Neue Conversation erstellen
        conversation = serializer.save(creator=creator)

        # Participants anlegen
        for user_id in participants:
            ConversationParticipant.objects.create(
                conversation=conversation,
                user_id=user_id
            )
        self.existing_conversation = conversation

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        convo = self.existing_conversation
        serializer = self.get_serializer(convo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(models.Q(creator=user) | models.Q(participants__user=user)).distinct()

class ConversationParticipantViewset(ModelViewSet):
    serializer_class = ConversationParticipantSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        conversation = Conversation.objects.get(id=conversation_id)

        # Nur der Creator darf Teilnehmer hinzufügen
        if conversation.creator != self.request.user:
            raise PermissionDenied("Only the creator can add participants.")

        user_id = self.request.data.get("user")
        user = User.objects.get(id=user_id)

        serializer.save(
            conversation=conversation,
            user=user
        )

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return ConversationParticipant.objects.filter(conversation_id=conversation_id)
