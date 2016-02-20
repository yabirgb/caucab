from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(blank=False, max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, related_name = "author")

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
        return self.message
