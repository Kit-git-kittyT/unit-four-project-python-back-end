from django.db import models
from django.contrib.auth.models import User
from datetime import date


CATEGORY =(
    ('A','Appreciation'),
    ('I', 'Impression'),
    ('G', 'Growth'),
    ('S', 'Suggestion'),
    ('D', 'Discussion')
)

class Interest(models.Model):
    passion= models.CharField(max_length=100)
    thrill= models.CharField(max_length=100)
    challenge= models.CharField(max_length=100)
    skill= models.CharField(max_length=100)
    past_experience= models.CharField(max_length=250)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.passion

class Comment(models.Model):
    text=models.CharField(max_length=20000)
    category=models.CharField(
        max_length=1,
        choices=CATEGORY,
        default=CATEGORY[0][0]
    )
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_comment_display()} by {self.user}'
