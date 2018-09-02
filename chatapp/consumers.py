from channels import Group
from channels.sessions import channel_session, enforce_ordering
from .models import Room
import json

@enforce_ordering
@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    # Message path if of form /chat/{label}
    prefix, label = message['path'].strip('/').split('/')
    room = Room.objects.get(label=label)
    # Add client to group of everyone in room
    Group('chat-'+label).add(message.reply_channel)
    # Persist room in channel's session for later
    message.channel_session['label'] = room.label

@enforce_ordering
@channel_session
def ws_receive(message):
    label = message.channel_session['label']
    room = Room.objects.get(label=label)
    data = json.loads(message['text'])
    m = room.messages.create(handle=data['handle'], message=data['message'])
    Group('chat-'+label).send({'text': json.dumps(m.as_dict())}, True)

@channel_session
def ws_disconnect(message):
    label = message.channel_session['label']
    Group('chat-'+label).discard(message.reply_channel)
