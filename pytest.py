import firebase_admin
from firebase_admin import credentials, messaging
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mapplate-version.json"

# cred = credentials.RefreshToken('mapplate-key.json')
default_app = firebase_admin.initialize_app()
# This registration token comes from the client FCM SDKs.
registration_token = 'fAON1gQsQEiVmmn_K6bCjZ'

# See documentation on defining a message payload.

message = messaging.Message(
    data={
        'score': '850',
        'time': '2:45',
    },
    token=registration_token,
)

# Send a message to the device corresponding to the provided
# registration token.
response = messaging.send(message)

# Response is a message ID string.
print('Successfully sent message:', response)