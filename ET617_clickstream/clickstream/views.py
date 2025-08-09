from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ClickstreamEvent
import json

@csrf_exempt
def track_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = ClickstreamEvent.objects.create(
                student_id=data.get('student_id', ''),
                action=data.get('action', ''),
                page_url=data.get('page_url', '')
            )
            return JsonResponse({'status': 'success', 'id': event.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

def view_events(request):
    events = list(ClickstreamEvent.objects.values())
    return JsonResponse(events, safe=False)
