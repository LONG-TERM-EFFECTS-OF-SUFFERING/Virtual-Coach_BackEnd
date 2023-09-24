from django.db import models

# Create your models here.

class Exercise(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField()
    img_url = models.CharField()

class Routine(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    time = models.BigIntegerField()
    exercises_number = models.IntegerField()
    exercise = models.ManyToManyField(Exercise, through='Routine_has_exercise', blank=True)

class User(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10)
    email = models.CharField(max_length=254, unique=True)

class User_has_Routine(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete = models.CASCADE)

class Routine_has_exercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete = models.CASCADE, blank=True, null=True)
    exercise = models.ForeignKey(Exercise, on_delete = models.CASCADE, blank=True, null=True)
    repetitions = models.IntegerField()
    series = models.IntegerField()
    rest = models.IntegerField()
