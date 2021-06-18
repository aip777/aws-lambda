from pusher_push_notifications import PushNotifications
import requests


beams_client = PushNotifications(
                instance_id='dj4vr7qITu-zKLJJ5lzVXR:',
                secret_key='AAAApGjplqU:',
                )

response = beams_client.publish_to_interests(
    interests=['hello'],
    publish_body={
        'apns': {
            'aps': {
                'alert': 'Hello!'
            }
        },
        'fcm': {
            'notification': {
                'title': 'Hello',
                'body': 'Hello, World!'
            }
        }
    }
)

print(response['publishId'])