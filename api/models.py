from django.db import models

# Create your models here.
class ApiModel(models.Model):
    image_uri = models.URLField(max_length=200)
    title = models.TextField(default=True)

    def __str__(self):
        return self.title

   