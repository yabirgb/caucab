from .models import Profile, Circle

def circles(request):
    if not request.user.is_anonymous():
        profile = Profile.objects.get(user = request.user)
        circles = Circle.objects.all().filter(owner = profile)

        return {'circles': circles}
    else:
        return {}
