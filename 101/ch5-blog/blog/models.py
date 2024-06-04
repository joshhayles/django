from django.db import models
from django.urls import reverse

# create a subclass of models.Model called "Post"
# each field under the class can be thought of as a column
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey( # defaults to a many-to-one relationship
        "auth.User",
        on_delete=models.CASCADE,
    )
    body = models.TextField() # used for larger amounts of text

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})