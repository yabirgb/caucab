from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django.core.urlresolvers import reverse

from .models import Message, Hashtag, Profile
from django.template import RequestContext

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#to make queries
from itertools import chain #join
from operator import attrgetter #used to order
from django.db.models import Q

# Create your views here.

def publish(request):
    if request.method == "POST":
        print("here1")
        if request.user.is_authenticated():
            text = request.POST["text"]
            author = Profile.objects.get(user=request.user)
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
                print(i[1:])
                p = Profile.objects.get(user__username = i[1:])
                message.mentions.add(p)
            print("here")
            message.save()

            response = {"text": text}
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print("Not loged")
            return redirect(reverse_lazy("login"))


def home(request):
    if not request.user.is_authenticated():
        return redirect(reverse_lazy('login'))
    profile = Profile.objects.get(user= request.user)

    messages_following = Message.objects.filter(Q(author = profile.following.all()))
    messages_own = Message.objects.filter(author = profile)
    messages = sorted(chain(messages_following, messages_own),key=attrgetter('created'), reverse = True)

    response = {}
    response["messages"] = messages
    return render_to_response("user/index.html", response, context_instance = RequestContext(request))

@login_required
def profile(request):
    response = {}
    if request.user.is_authenticated():
        profile = Profile.objects.get(user = request.user)
        messages = Message.objects.all().filter(author = profile).order_by("-pk")
        response["messages"] = messages

    return render_to_response("user/profile.html", response, RequestContext(request))
