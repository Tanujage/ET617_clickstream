from rest_framework import serializers
from .models import Event, QuizAttempt

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','user','session_id','event_type','content','event_time','event_props','created_at']
        read_only_fields = ['id','created_at','event_time']

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id','user','quiz','answers','score','duration_seconds','attempted_at']
        read_only_fields = ['id','attempted_at','user']
