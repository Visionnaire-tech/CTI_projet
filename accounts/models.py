from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='teacher_profile'
)
    def __str__(self):
        return self.user.username

    