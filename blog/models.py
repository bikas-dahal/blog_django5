from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.functions import Now



class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    # publish = models.DateTimeField(default=timezone.now)
    publish = models.DateTimeField(db_default=Now())    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )   
    
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    
    def __str__(self):
        return self.title
    
    