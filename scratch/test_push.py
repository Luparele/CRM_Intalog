import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM_Comercial.settings')
django.setup()

from webpush.models import PushInformation
from webpush import send_user_notification

push_infos = PushInformation.objects.all()
print(f"Found {len(push_infos)} subscriptions")

for p in push_infos:
    user = p.user
    print(f"Sending to user: {user.username}")
    try:
        send_user_notification(user=user, payload={"head": "test", "body": "test"}, ttl=1000)
        print("Success for", user.username)
    except Exception as e:
        print(f"Failed for {user.username}:")
        print(traceback.format_exc())
