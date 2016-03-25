from django.shortcuts import render
from django.shortcuts import render_to_response,redirect, get_object_or_404
from django.core.urlresolvers import reverse

from .models import Message, Hashtag, Profile, Notification, Circle
from django.contrib.auth.models import User
from django.template import RequestContext

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#to make queries
from itertools import chain #join
from operator import attrgetter #used to order
from django.db.models import Q

def get_user(u):
    return Profile.objects.get(user = u)

def publish(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            text = request.POST["text"]
            if len(text) > 180:
                return redirect(request.META.get('HTTP_REFERER'))
            author = get_user(request.user)
            message = Message(message= text, author= author)
            message.save()

            #Hashtags
            has = message.get_hashtag()
            for i in has:
                obj, created = Hashtag.objects.get_or_create(name = i[1:])
                message.hashtag.add(obj)

            #mentions
            men = message.get_mentions()
            for i in men:
                try:
                    p = Profile.objects.get(user__username = i[1:])
                    message.mentions.add(p)
                    notification = Notification(origin=author, objetive=p, category = 3, message= message)
                    notification.save()
                except:
                    error = "user doesn't exist"
                    print(error)
            message.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print("Not loged")
            return redirect(reverse_lazy("login"))

@login_required
def home(request):
    profile = get_user(request.user)

    messages_following = Message.objects.filter(author__in=[member for member in profile.following.all()])
    messages_own = Message.objects.filter(author = profile)
    messages = sorted(chain(messages_following, messages_own),key=attrgetter('created'), reverse = True)

    response = {}
    response["messages"] = messages
    response["profile"] = profile
    return render(request, "user/index.html", response)

@login_required
def profile(request):
    response = {}
    profile = get_user(request.user)
    messages = Message.objects.filter(author = profile).order_by("-pk")

    response["messages"] = messages
    response["profile"] = profile

    return render(request,"user/profile.html", response)

@login_required
def notifications(request):
    profile = get_user(request.user)
    notifications = Notification.objects.all().filter(objetive = profile).order_by("-pk")

    response = {"messages":notifications, "profile": profile}
    return render(request, "user/notifications.html", response)
@login_required
def circle(request, circle_id):
    response={}
    circle = get_object_or_404(Circle, identificator = circle_id)
    messages = Message.objects.all().filter(author__in=[member for member in circle.members.all()])

    response["messages"] = messages
    return render(request, "user/index.html", response)

def profile(request, username):
    response = {}
    user = get_object_or_404(User, username = username)
    profile = get_object_or_404(Profile, user = user)

    messages = Message.objects.filter(author = profile).order_by("-pk")

    response["profile"] = profile
    response["messages"] = messages
    return render(request, "user/profile.html", response)
