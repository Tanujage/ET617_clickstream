from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Content(models.Model):
    TYPE_CHOICES = [
        ('text', 'Text'),
        ('video', 'Video'),
        ('quiz', 'Quiz'),
        ('mixed', 'Mixed'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    body = models.TextField(blank=True)   # HTML or markdown rendered as safe
    video_url = models.URLField(blank=True, null=True)  # for video content / embed link
    metadata = models.JSONField(blank=True, null=True)  # any extra metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE, related_name='quiz')
    # questions stored as list of objects: [{id, question, choices:[...], correct_index:0}]
    questions = models.JSONField()

    def __str__(self):
        return f"Quiz for {self.content.title}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    answers = models.JSONField()  # {question_id: selected_index}
    score = models.FloatField()
    duration_seconds = models.IntegerField(null=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    # Clickstream event
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=128, null=True, blank=True)
    event_type = models.CharField(max_length=64)  # e.g., page_view, click, video_play
    content = models.ForeignKey(Content, on_delete=models.SET_NULL, null=True, blank=True)
    event_time = models.DateTimeField(auto_now_add=True)
    event_props = models.JSONField(null=True, blank=True)  # store full payload (coords, video_time)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'event_time']),
            models.Index(fields=['content']),
        ]
