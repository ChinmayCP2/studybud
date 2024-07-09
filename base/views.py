from django.shortcuts import render, redirect
# Create your views here.
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
# Q is used to do and OR in filter 
# rooms = [
#     {'id': 1 , 'name' : 'py'},
#     {'id': 2 , 'name' : 'json'},
#     {'id': 3 , 'name' : 'java'},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''

    topics = Topic.objects.all()  
    rooms = Room.objects.filter(Q(topic__name__contains = q) |
                                 Q(name__icontains = q) | Q(description__contains = q))
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count' : room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        # instance = room is there so we dont create a new form but update the existing one
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' : room})