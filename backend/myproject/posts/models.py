from django.db import models

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=150)
  content = models.CharField(max_length=2000)

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  comment = models.TextField()
  created_on = models.DateTimeField()
  updated_on = models.DateTimeField(auto_now=True)

  class Meta:
   db_table = "comments"