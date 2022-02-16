from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse


# # #====================================================
# import pyttsx3 #pip install pyttsx3
# import datetime
#=========================================== 
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# # print(voices[1].id)
# engine.setProperty('voice', voices[1].id)


# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()

# def wishMe():
#     hour = int(datetime.datetime.now().hour)
#     if hour>=0 and hour<12:
#         speak("Good Morning!")

#     elif hour>=12 and hour<18:
#         speak("Good Afternoon!")   

#     else:
#         speak("Good Evening!")  
    
#     speak("Welcome to chat, please enter your name and room id")
#================================================
# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {
        "rooms" : rooms
    }
    # wishMe()
    # speak("Welcome to chat, please enter your name and room id")
    return render(request, 'home.html', context)

def room(request, room):
    # speak('Welcome to chat section')
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })
    # return render(request, 'home.html')

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

# def EditUser(request, room):
#     username =  request.POST['EditUsername']
#     return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    if len(message) > 0:
        new_message = Message.objects.create(value=message, user=username, room=room_id)
        new_message.save()
        print("Message Size:",len(message))
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})