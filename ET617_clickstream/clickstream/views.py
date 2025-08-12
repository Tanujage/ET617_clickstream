# clickstream/views.py
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import ClickEvent
from .forms import RegisterForm
from django.contrib.auth import get_user_model
User = get_user_model()


def home_view(request):
    return render(request, 'quiz_home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            messages.success(request, "Account created. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('email') or request.POST.get('loginEmail')
        password = request.POST.get('password') or request.POST.get('loginPassword')
        # try login by username first, then by email
        user = authenticate(request, username=username, password=password)
        if user is None:
            # try authenticate by email
            try:
                u = User.objects.get(email__iexact=username)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = None
        if user is not None:
            login(request, user)
            return redirect('quiz_home')
        messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def quiz_view(request):
    return render(request, 'quiz.html')

@login_required
def video_view(request):
    return render(request, 'video.html')

# API endpoint to collect clickstream events
@csrf_exempt
def collect_click_event(request):
    print("collect_click_event CALLED")
    print("METHOD:", request.method)
    print("BODY:", request.body)

    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST.dict() or {}

    event_type = data.get('event_type') or data.get('type')
    path = data.get('path') or request.META.get('HTTP_REFERER','')
    meta = data.get('meta', {})
    user_agent = request.META.get('HTTP_USER_AGENT','')
    ip = request.META.get('REMOTE_ADDR','')

    user = None
    if request.user.is_authenticated:
        user = request.user
    else:
        uid = data.get('user_id')
        if uid:
            try:
                user = User.objects.filter(id=uid).first()
            except:
                user = None

    evt = ClickEvent.objects.create(
        user=user,
        path=path,
        event_type=event_type or 'unknown',
        user_agent=user_agent[:500],
        ip_address=ip,
        meta=meta
    )
    return JsonResponse({'status':'ok','id': evt.id})
