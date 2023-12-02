from django.test import TestCase
from django.urls import reverse, resolve
from routines.models import *
from routines.views import *
from accounts.models import *

class TestUrls(TestCase):
    def test_url_exercise_view(self):
        url = reverse('Exercise-list')
        self.assertEquals(resolve(url).func.cls, ExerciseView)

    def test_url_routine_view(self):
        url = reverse('Routine-list')
        self.assertEquals(resolve(url).func.cls, RoutineView)

    def test_url_user_has_routine_view(self):
       url = reverse('User_has_Routine-list')
       self.assertEquals(resolve(url).func.cls, User_has_RoutineView)

    def test_url_routine_has_exercise_view(self):
        url = reverse('Routine_has_exercise-list')
        self.assertEquals(resolve(url).func.cls, Routine_has_exerciseView)
    
    def test_url_get_user_routines(self):
       url = reverse('get_user_routines', args=[1])
       self.assertEquals(resolve(url).func, get_user_routines)

    def test_url_get_routine_exercises(self):
        url = reverse('get_routine_exercises', args=[1])
        self.assertEquals(resolve(url).func, get_routine_exercises)

    def test_edit_routine(self):
        url = reverse('edit_a_routine', args=[1])
        self.assertEquals(resolve(url).func, edit_routine)