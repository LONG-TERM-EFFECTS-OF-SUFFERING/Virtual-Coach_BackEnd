from django.db import models
from accounts.models import UserAccount as User


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    img_url = models.CharField()
    def __str__(self):
        return self.name

class Routine(models.Model):
    name = models.CharField(max_length=255, default="My routine")
    time = models.BigIntegerField()
    description = models.CharField(max_length=255, null=True)
    exercises_number = models.IntegerField()
    exercise = models.ManyToManyField(Exercise, through='Routine_has_exercise', blank=True)
    def __str__(self):
        return "routine #"+str(self.id)

class User_has_Routine(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('user', 'routine')

class Routine_has_exercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete = models.CASCADE, blank=True, null=True)
    exercise = models.ForeignKey(Exercise, on_delete = models.CASCADE, blank=True, null=True)
    repetitions = models.IntegerField()
    series = models.IntegerField()
    rest = models.IntegerField()
