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



def get_upload_path(instance, filename):
        return f'podcasts/{instance.podcast.slug}/{instance.slug}/'

class PodcastEpisode(AbstractContent):
    speakers = models.ManyToManyField(User, related_name='podcast_episodes')
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    file = models.FileField(upload_to=get_upload_path, validators=[FileExtensionValidator(['mp3', 'aac', 'wav'])])    


class Video(AbstractContent):
    pass


class Image(AbstractContent):
    pass


class Entry(AbstractContent):
    pass



