import json

from django.conf import settings
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from webpush import send_user_notification


def forbidden_403(request, template_name='403.html'):
    return render(request, template_name, status=403)


def page_not_found_404(request, template_name='404.html'):
    return render(request, template_name, status=404)


def error_500(request, template_name='500.html'):
    return render(request, template_name, status=500)


@require_GET
def push_notification(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})  # assigned the value of the WEBPUSH_SETTINGS attribute
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    # user-this variable comes from the incoming request,
    # whenever a user makes a request to the server, the details for that user are stored in the user field

    return render(request, 'push_notification.html', {user: user, 'vapid_key': vapid_key})   # notification.html


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body  # the body of the notification, head-the title of the push notification
        data = json.loads(body)  # json.loads takes a structured JSON document and converts it to Python object

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']  # id of the request user
        user = get_object_or_404(User, pk=user_id)  # the recipient of the push notification
        payload = {'head': data['head'], 'body': data['body']}  # the notification info which includes the head and body
        send_user_notification(user=user, payload=payload, ttl=1000)
        # ttl- the max. time in sec that the notification should be stored if the user is offline
        return JsonResponse(status=200, data={'message': 'Web push successful'})

    except TypeError:
        return JsonResponse(status=500, data={'message': 'An error occurred'})

