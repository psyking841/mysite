from django.db import models
from django.template import loader

# Create your models here.

class NewsFeed(models.Model):
    news_source = models.CharField(max_length=32)
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    pub_date = models.DateTimeField(auto_now=False)
    article_type = models.CharField(max_length=32)
    language = models.CharField(max_length=5)
    sentiment = models.CharField(max_length=1024)

    def render(self):
        self.render_text = self.description.replace('\n', '<br>')
        template = loader.get_template('theora/post.html')
        return template.render({'p': self})

class User(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=512)
    email = models.CharField(max_length=128)