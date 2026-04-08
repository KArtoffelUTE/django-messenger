from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'conversations', ConversationViewset, basename='conversation')

conversations_nested = [
    path('<int:conversation_id>/messages/', MessageViewset.as_view({'get': 'list', 'post': 'create'})),
    path('<int:conversation_id>/participants/', ConversationParticipantViewset.as_view({'get': 'list', 'post': 'create'})),
]

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/', include(conversations_nested)),
]