import os
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class AbstractContent(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        abstract = True


class Podcast(AbstractContent):
    pass



def podcast_episode_path(instance, filename):
    return os.path.join('podcasts', instance.podcast.slug, instance.slug, filename)

class PodcastEpisode(AbstractContent):
    speakers = models.ManyToManyField(User, related_name='podcast_episodes')
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    file = models.FileField(upload_to=podcast_episode_path, validators=[FileExtensionValidator(['mp3', 'aac', 'wav'])])    


class Video(AbstractContent):
    file = models.FileField(upload_to='videos', validators=[FileExtensionValidator(['mp4', 'avi', 'mkv'])])


class Image(AbstractContent):
    file = models.ImageField(upload_to='images')



class Entry(AbstractContent):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')




