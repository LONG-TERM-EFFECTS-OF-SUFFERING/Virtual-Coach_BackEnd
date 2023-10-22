from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import ExerciseSerializer
from .serializer import RoutineSerializer
from .serializer import User_has_RoutineSerializer
from .serializer import Routine_has_exerciseSerializer
from .models import Exercise
from .models import Routine
from .models import User_has_Routine
from .models import Routine_has_exercise


class ExerciseView(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()

class RoutineView(viewsets.ModelViewSet):
    serializer_class = RoutineSerializer
    queryset = Routine.objects.all()

class User_has_RoutineView(viewsets.ModelViewSet):
    serializer_class = User_has_RoutineSerializer
    queryset = User_has_Routine.objects.all()

class Routine_has_exerciseView(viewsets.ModelViewSet):
    serializer_class = Routine_has_exerciseSerializer
    queryset = Routine_has_exercise.objects.all()


@api_view(['GET'])
def get_user_routines(request, email):
    queryset = User_has_Routine.objects.all()
    user_routines = queryset.filter(user__email = email)
    serializer = User_has_RoutineSerializer(user_routines, many=True)
    print(queryset)

    return Response(serializer.data)

@api_view(['GET'])
def get_routine_exercises(request, routine):
    queryset = Routine_has_exercise.objects.all()
    routine_exercises = queryset.filter(routine_id = routine)
    serializer = Routine_has_exerciseSerializer(routine_exercises)
    print(queryset)

    return Response(serializer.data)
