from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from routines.models import Exercise, Routine, User_has_Routine, Routine_has_exercise
from accounts.models import UserAccount

class TestExerciseView(TestCase):
    def test_list_exercises(self):
        url = reverse('Exercise-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestRoutineView(TestCase):
    def setUp(self):
        self.testExercise = Exercise.objects.create(
        name = 'TestExercise',
        img_url = '/TestPicture.png',
        )

        self.testRoutine = Routine.objects.create(
        name = 'TestRoutine',
        time = 1,
        description = 'TestDescription',
        exercises_number = 1,
        )
    
    def test_list_routines(self):
        url = reverse('Routine-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_routine_with_exercises(self):
        routine_id = self.testRoutine.id
        url = reverse('Routine-detail', args=[routine_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestUser_has_RoutineView(TestCase):
    def setUp(self):
        self.test_user = UserAccount.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword'
        )

        self.testExercise = Exercise.objects.create(
        name = 'TestExercise',
        img_url = '/TestPicture.png',
        )

        self.testRoutine = Routine.objects.create(
        name = 'TestRoutine',
        time = 1,
        description = 'TestDescription',
        exercises_number = 1,
    )

    def test_create_user_has_routine(self):
        user_id = self.test_user.id
        routine_id = self.testRoutine.id
        url = reverse('User_has_Routine-list')
        data = {'user': user_id, 'routine': {'id': routine_id}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestRoutine_has_exerciseView(TestCase):
    def test_list_routine_has_exercises(self):
        url = reverse('Routine_has_exercise-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
