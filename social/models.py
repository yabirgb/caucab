from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(blank=False, max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name = "author")
    following = models.ManyToManyField("self", related_name = "following", blank= True)
    followers = models.ManyToManyField("self", related_name = "followers", blank= True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.author.user.username, filename)

    message = models.CharField(blank=False, max_length=180)
    author = models.ForeignKey(Profile, related_name = "author")
    mentions = models.ManyToManyField(Profile, related_name = "mentions", blank = True)
    hashtag = models.ManyToManyField(Hashtag, blank = True)
    likes = models.IntegerField(blank=True, null=True)
    favorites = models.IntegerField(blank=True, null=True)
    image1 = models.ImageField(upload_to=user_directory_path, blank= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_hashtag(self):
        hashtags = [has for has in self.message.split(" ") if has[0] == "#"]
        return hashtags

    def get_mentions(self):
        mentions = [mention for mention in self.message.split(" ") if mention[0] == "@"]
        return mentions

    def save(self, *args, **kwargs):
        #if not self.pk:
        #This code only happens if the objects is
        #not in the database yet. Otherwise it would
        #have pk
            #self.get_hashtag()
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return self.message + " by " + self.author.user.username

class Notification(models.Model):

    CATEGORIES = (
        (0, "Like"),
        (1, "Repeat"),
        (2, "Follow"),
        (3, "Mention")
    )

    origin = models.ForeignKey(Profile, related_name= "origin")
    objetive = models.ForeignKey(Profile, related_name= "objetive")
    category = models.IntegerField(choices = CATEGORIES)
    message = models.ForeignKey(Message, related_name= "message_refered", blank = True, null = True)

    def __str__(self):
        return str(self.CATEGORIES[self.category][1])

class Circle(models.Model):
    colors = (
        ("red darken-1","red"),#red
        ("purple darken-1","purple"),#purple
        ("white","white"),
        ("blue darken-1","blue")#blue
    )

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Profile, related_name = "owner")
    members = models.ManyToManyField(Profile, blank = True)
    color = models.CharField(choices = colors, max_length= 30)

    def __str__(self):
        return str(self.name)
