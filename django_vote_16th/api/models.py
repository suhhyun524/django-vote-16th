from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    user_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    part = models.CharField(max_length=30)
    password = models.CharField(max_length=150)
    team = models.CharField(max_length=30)
    is_voted_demo = models.BooleanField(default=False)
    is_voted_partleader = models.BooleanField(default=False)

    def __str__(self):
        return self.name