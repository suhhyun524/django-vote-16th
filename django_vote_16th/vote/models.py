from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Demo_Vote(BaseModel):
    team = models.CharField(max_length=30)

    def __str__(self):
        return self.team


class PartLeader_Vote(BaseModel):
    part = models.CharField(max_length=30)
    votee = models.CharField(max_length=30)

    def __str__(self):
        return self.votee
