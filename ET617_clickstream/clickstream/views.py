from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Content, Event, Quiz, QuizAttempt
from .serializers import EventSerializer, QuizAttemptSerializer

# simple register and login views (template-based)
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('courses:index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('courses:index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def index(request):
    contents = Content.objects.all().order_by('created_at')
    return render(request, 'index.html', {'contents': contents})

def content_detail(request, slug):
    content = get_object_or_404(Content, slug=slug)
    quiz = getattr(content, 'quiz', None)
    return render(request, 'content_detail.html', {'content': content, 'quiz': quiz})

# API endpoints (DRF function-based)
@api_view(['POST'])
@permission_classes([AllowAny])
def ingest_events(request):
    """
    Accepts a batch: { events: [ {...}, {...} ] }
    Each event should contain: event_type, session_id, content (id), event_props, event_time (optional)
    """
    payload = request.data
    events = payload.get('events', [])
    saved = []
    for ev in events:
        # Try to map user if provided or anonymous
        user = None
        user_id = ev.get('user_id')
        if user_id:
            from django.contrib.auth import get_user_model
            try:
                user = get_user_model().objects.get(pk=user_id)
            except Exception:
                user = None
        content_obj = None
        content_id = ev.get('content_id') or ev.get('content')
        if content_id:
            try:
                content_obj = Content.objects.get(pk=content_id)
            except Content.DoesNotExist:
                content_obj = None
        e = Event.objects.create(
            user=user,
            session_id=ev.get('session_id'),
            event_type=ev.get('event_type','unknown'),
            content=content_obj,
            event_props=ev.get('event_props', {})
        )
        saved.append(e.id)
    return Response({'inserted': len(saved)}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def quiz_attempt_view(request):
    # requires auth to create attempt (you may allow anonymous too)
    serializer = QuizAttemptSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
