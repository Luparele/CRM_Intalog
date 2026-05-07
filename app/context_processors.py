from django.conf import settings

def webpush_settings(request):
    return {
        'WEBPUSH_PUBLIC_KEY': settings.WEBPUSH_SETTINGS.get('VAPID_PUBLIC_KEY')
    }
