from .models import Profile, Circle

def circles(request):
    profile = Profile.objects.get(user = request.user)
    circles = Circle.objects.all().filter(owner = profile)

    return {'circles': circles}
