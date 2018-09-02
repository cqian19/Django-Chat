from django.shortcuts import render, redirect
from django.db import transaction
from .models import Room
import haikunator

def about(request):
    return render(request, "chat/about.html")

def chat_room(request, label):
    room, created = Room.objects.get_or_create(label=label)

    # Get 50 most recent messages
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages
    })

def new_room(request):
    name_generator = haikunator.Haikunator()
    new_room = None
    while not new_room:
        with transaction.atomic():
            name = name_generator.haikunate()
            if Room.objects.filter(label=name).exists():
                continue
            new_room = Room.objects.create(label=name)
    return redirect(chat_room, label=name)