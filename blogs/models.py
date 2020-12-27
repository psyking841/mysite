from django.db import models
from django.template import loader


class User(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=512)
    email = models.CharField(max_length=128)


class Post(models.Model):
    subject = models.CharField(max_length=128)
    content = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def render(self):
        self.render_text = self.content.replace('\n', '<br>')
        template = loader.get_template('blogs/post.html')
        return template.render({'p': self})
