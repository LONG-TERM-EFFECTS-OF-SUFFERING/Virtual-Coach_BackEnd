from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from routines.models import Exercise, Routine, User_has_Routine, Routine_has_exercise
from accounts.models import UserAccount

class TestExerciseView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_exercise = Exercise.objects.create(
            name='TestExercise',
            img_url = '/TestPicture.phg'
        )
    
    def test_list_exercises(self):
        url = reverse('Exercise-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_exercise(self):
        url = reverse('Exercise-list')
        new_exercise_data = {
            'name': 'NewExercise',
            'img_url': '/NewPicture.png',
        }
        response = self.client.post(url, new_exercise_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Exercise.objects.filter(name='NewExercise').exists())

    def test_read_exercise_list(self):
        url = reverse('Exercise-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.test_exercise.name)

    def test_read_single_exercise(self):
        url = reverse('Exercise-detail', args=[self.test_exercise.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.test_exercise.name)

    def test_update_exercise(self):
        url = reverse('Exercise-detail', args=[self.test_exercise.id])
        updated_data = {
            'name': 'UpdatedExercise',
            'img_url': '/UpdatedPicture.png',
        }
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_exercise.refresh_from_db()
        self.assertEqual(self.test_exercise.name, 'UpdatedExercise')

    def test_delete_exercise(self):
        url = reverse('Exercise-detail', args=[self.test_exercise.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Exercise.objects.filter(id=self.test_exercise.id).exists())

class TestRoutineView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.test_user = UserAccount.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword'
        )

        # Create an exercise
        self.test_exercise = Exercise.objects.create(
            name='TestExercise',
            img_url='/TestPicture.png',
        )

        # Create a routine without directly passing exercises
        self.test_routine = Routine.objects.create(
            name='TestRoutine',
            time=1,
            description='TestDescription',
            exercises_number=1,
        )

        # Associate exercises with the routine using Routine_has_exercise
        self.Routine_has_exercise = Routine_has_exercise.objects.create(
            routine = self.test_routine,
            exercise = self.test_exercise,
            repetitions = 10,
            series = 3,
            rest = 60,
        )


    def test_create_routine(self):
        url = reverse('Routine-list')
        new_routine_data = {
            'name': 'NewRoutine',
            'time': 2,
            'description': 'NewDescription',
            'exercises_number': 2,
            'exercises': [{'exercise': self.test_exercise.id, 'repetitions': 12, 'series': 4, 'rest': 45}],
        }
        response = self.client.post(url, new_routine_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Routine.objects.filter(name='NewRoutine').exists())

    def test_read_routine_list(self):
        url = reverse('Routine-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.test_routine.name)

    def test_read_single_routine(self):
        url = reverse('Routine-detail', args=[self.test_routine.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.test_routine.name)

    def test_update_routine(self):
        url = reverse('Routine-detail', args=[self.test_routine.id])
        updated_data = {
            'name': 'UpdatedRoutine',
            'time': 3,
            'description': 'UpdatedDescription',
            'exercises_number': 3,
            'exercises': [{'exercise': self.test_exercise.id, 'repetitions': 15, 'series': 5, 'rest': 30}],
        }
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_routine.refresh_from_db()
        self.assertEqual(self.test_routine.name, 'UpdatedRoutine')

    def test_delete_routine(self):
        url = reverse('Routine-detail', args=[self.test_routine.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Routine.objects.filter(id=self.test_routine.id).exists())

    #Endpoints from developer
    def test_get_user_routines(self):
        url = reverse('get_user_routines', args=[self.test_user.email])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_routine_exercises(self):
        url = reverse('get_routine_exercises', args=[self.test_routine.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestUser_has_RoutineView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.test_user = UserAccount.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword'
        )

        self.test_exercise = Exercise.objects.create(
            name='TestExercise',
            img_url='/TestPicture.png',
        )

        self.test_routine = Routine.objects.create(
            name='TestRoutine',
            time=1,
            description='TestDescription',
            exercises_number=1,
        )

        self.test_user_has_routine = User_has_Routine.objects.create(
            user = self.test_user,
            routine = self.test_routine
        )

    def test_create_user_has_routine(self):
        url = reverse('User_has_Routine-list')
        data = {'user': self.test_user.id, 'routine': {'id': self.test_routine.id}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_user_has_routine_list(self):
        url = reverse('User_has_Routine-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_single_user_has_routine(self):
        user_has_routine_id = self.test_user_has_routine.id  
        url = reverse('User_has_Routine-detail', args=[user_has_routine_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_user_has_routine(self):
        user_has_routine = self.test_user_has_routine
        url = reverse('User_has_Routine-detail', args=[user_has_routine.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User_has_Routine.objects.filter(id=user_has_routine.id).exists())

class TestRoutine_has_exerciseView(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create an exercise
        self.test_exercise = Exercise.objects.create(
            name='TestExercise',
            img_url='/TestPicture.png',
        )

        # Create a routine
        self.test_routine = Routine.objects.create(
            name='TestRoutine',
            time=1,
            description='TestDescription',
            exercises_number=1,
        )

        # Create a routine_has_exercise instance
        self.test_routine_has_exercise = Routine_has_exercise.objects.create(
            routine=self.test_routine,
            exercise=self.test_exercise,
            repetitions=10,
            series=3,
            rest=60,
        )

    def test_list_routine_has_exercises(self):
        url = reverse('Routine_has_exercise-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data based on your expected structure

    def test_create_routine_has_exercise(self):
        url = reverse('Routine_has_exercise-list')
        new_routine_has_exercise_data = {
            'routine': self.test_routine.id,
            'exercise': self.test_exercise.id,
            'repetitions': 15,
            'series': 4,
            'rest': 45,
        }
        response = self.client.post(url, new_routine_has_exercise_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assert the created routine_has_exercise instance

    def test_read_routine_has_exercise_list(self):
        url = reverse('Routine_has_exercise-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data based on your expected structure

    def test_read_single_routine_has_exercise(self):
        url = reverse('Routine_has_exercise-detail', args=[self.test_routine_has_exercise.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data based on your expected structure

    def test_update_routine_has_exercise(self):
        url = reverse('Routine_has_exercise-detail', args=[self.test_routine_has_exercise.id])
        updated_data = {
            'routine': self.test_routine.id,
            'exercise': self.test_exercise.id,
            'repetitions': 20,
            'series': 5,
            'rest': 30,
        }
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the updated routine_has_exercise instance

    def test_delete_routine_has_exercise(self):
        url = reverse('Routine_has_exercise-detail', args=[self.test_routine_has_exercise.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Routine_has_exercise.objects.filter(id=self.test_routine_has_exercise.id).exists())
