from django.db import models
from users.models import CustomUser

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="blogs")
    image = models.ImageField(upload_to="blog_images/")


    def __str__(self):
        return self.title