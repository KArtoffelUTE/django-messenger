from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Conversation(models.Model):
    name = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Conversation {self.typ} at {self.timestamp}'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Message from {self.sender.username} in Conversation {self.conversation.id} at {self.timestamp}'

class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_participated')

    def __str__(self):
        return f'{self.user.username} in {self.conversation.name}'