from django.db import models

# Model to store conversation history.
# MongoDB is document-based, so storing the message pairs as documents is efficient.
class ChatHistory(models.Model):
    # Field to link the conversation to a specific user (required for multi-user apps)
    session_id = models.CharField(max_length=100, unique=True, verbose_name="User Session ID")
    
    # A list of objects/documents to store the conversation flow
    # Djongo automatically handles converting lists of dictionaries into MongoDB sub-documents.
    messages = models.JSONField(default=list) 
    
    # Timestamp for the last activity
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat Session: {self.session_id}"
    
    class Meta:
        verbose_name_plural = "Chat Histories"
