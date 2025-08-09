from django.contrib import admin
from .models import Content, Quiz, QuizAttempt, Event

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title','type','slug','created_at')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('content',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user','quiz','score','attempted_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','user','event_type','content','event_time')
    readonly_fields = ('event_props',)
