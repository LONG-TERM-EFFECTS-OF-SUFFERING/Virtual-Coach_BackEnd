from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, serializers, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import DynamicDepthSerializer
from .serializer import ExerciseSerializer
from .serializer import RoutineSerializer
from .serializer import User_has_RoutineSerializer
from .serializer import Routine_has_exerciseSerializer
from .serializer import RoutineExercisesSerializer
from .models import Exercise
from .models import Routine
from .models import User_has_Routine
from .models import Routine_has_exercise

from accounts.models import UserAccount


class DynamicDepthViewSet(viewsets.ModelViewSet):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        depth = 0

        try:
            depth = int(self.request.query_params.get('depth', 0))
        except ValueError:
            pass # Ignore non-numeric parameters and keep default 0 depth

        context['depth'] = depth

        return context

class ExerciseView(DynamicDepthViewSet):
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()

class RoutineView(DynamicDepthViewSet):
    serializer_class = RoutineSerializer
    queryset = Routine.objects.all()

    def retrieve(self, request, pk=None):
        routine = get_object_or_404(Routine, pk=pk)
        exercises = Routine_has_exercise.objects.defer("routine").filter(routine=pk)
        serializer_exercises = RoutineExercisesSerializer(exercises, many=True)
        serializer_routine = RoutineSerializer(routine)
        response = serializer_routine.data
        response['exercise'] = serializer_exercises.data
        return Response(response)

class User_has_RoutineView(DynamicDepthViewSet):
    serializer_class = User_has_RoutineSerializer
    queryset = User_has_Routine.objects.all()

    def create(self, request):
        data = request.data
        user_id = data['user']
        user = get_object_or_404(UserAccount, pk=user_id)
        routine = data['routine']
        routineSerializer = RoutineSerializer(data=routine)
        if (routineSerializer.is_valid()):
            routineSaved = routineSerializer.save()
            user_has_routine = User_has_Routine(user=user, routine=routineSaved)
            user_has_routine.save()
            return Response(routineSerializer.data)
        else:
            return Response(routineSerializer.errors)

class Routine_has_exerciseView(DynamicDepthViewSet):
    serializer_class = Routine_has_exerciseSerializer
    queryset = Routine_has_exercise.objects.all()


@api_view(['GET'])
def get_user_routines(request, id):
    queryset = User_has_Routine.objects.all()
    user_routines = queryset.filter(user__id = id)
    routines = [user_routine.routine for user_routine in user_routines]

    depth = 0

    try:
        depth = int(request.query_params.get('depth', 0))
    except ValueError:
        pass # Ignore non-numeric parameters and keep default 0 depth

    serialized = RoutineSerializer(routines, many=True, context={'depth': depth})

    return Response(serialized.data)

@api_view(['GET'])
def get_routine_exercises(request, routine):
    routines_objects = Routine.objects.all()
    routine_object = routines_objects.get(id = routine)
    exercises = routine_object.exercise.all()
    serialized = ExerciseSerializer(exercises, many=True)

    return Response(serialized.data)

@api_view(['PATCH', 'PUT'])
def edit_routine(request, routine):
    request_data = request.data
    routine_object = get_object_or_404(Routine, pk=routine)


    if 'name' in request_data or 'description' in request_data:
        routine_data = { 'name' : request_data['name'], 'description' : request_data['description'] }

        serializer = RoutineSerializer(instance = routine_object, data = routine_data)

        if serializer.is_valid():
            serializer.save()
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if 'exercises' in request_data:

        exercises_data = request_data['exercises']

        existing_exercises = routine_object.exercise.all()
        existing_exercises_ids = [exercise.id for exercise in existing_exercises]

        for exercise_data in exercises_data:
            exercise_id = exercise_data.get('id')

            if exercise_id in existing_exercises_ids:
                exercise = get_object_or_404(Exercise, pk=exercise_id)
                serializer = ExerciseSerializer(instance = exercise, data = exercise_data)

            if serializer.is_valid():
                serializer.save()
            else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serialized = RoutineSerializer(routine_object)

    return  Response(serialized.data)
