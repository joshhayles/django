from django.db import models

# this creates a new database model called 'Post,' which has the database field 'text' with the type of content being TextField()
class Post(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50] # returns the string / text visual for better readability