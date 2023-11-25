from django.test import TestCase
from routines.models import Exercise, Routine, User_has_Routine, Routine_has_exercise
from routines.views import *

class TestModels(TestCase):

  #Setup
  #------------------------------------------------------
  def setUp(self):

    #Creation of Test exercise
    self.testExercise = Exercise.objects.create(
      name = 'TestExercise',
      img_url = '/TestPicture.png',
      )

    #Creation of Test routine
    self.testRoutine = Routine.objects.create(
      name = 'TestRoutine',
      time = 1,
      description = 'TestDescription',
      exercises_number = 1,
    )

    #Creation of Test 'routine_has_exercise'
    self.testRoutine_has_exercise = Routine_has_exercise.objects.create(
          routine=self.testRoutine,
          exercise=self.testExercise,
          repetitions=3,
          series=4,
          rest=60,
      )

  #Tests for models
  def test_exercise_properties(self):
    expected_values = {
       'name': 'TestExercise',
       'img_url': '/TestPicture.png'
    }
    for field, value in expected_values.items():
          self.assertEqual(getattr(self.testExercise, field), value)

  def test_routine_properties(self):
      expected_values = {
       'name': 'TestRoutine',
       'time': 1,
       'description': 'TestDescription',
       'exercises_number': 1
      }
      for field, value in expected_values.items():
          self.assertEqual(getattr(self.testRoutine, field), value)

  def test_routine_has_exercise(self):
      expected_values = {
          'routine': self.testRoutine,
          'exercise': self.testExercise,
          'repetitions': 3,
          'series': 4,
          'rest': 60,
      }
      for field, value in expected_values.items():
          self.assertEqual(getattr(self.testRoutine_has_exercise, field), value)