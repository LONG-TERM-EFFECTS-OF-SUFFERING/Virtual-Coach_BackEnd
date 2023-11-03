from rest_framework import viewsets, serializers, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import DynamicDepthSerializer
from .serializer import ExerciseSerializer
from .serializer import RoutineSerializer
from .serializer import User_has_RoutineSerializer
from .serializer import Routine_has_exerciseSerializer
from .models import Exercise
from .models import Routine
from .models import User_has_Routine
from .models import Routine_has_exercise


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

class User_has_RoutineView(DynamicDepthViewSet):
    serializer_class = User_has_RoutineSerializer
    queryset = User_has_Routine.objects.all()

class Routine_has_exerciseView(DynamicDepthViewSet):
    serializer_class = Routine_has_exerciseSerializer
    queryset = Routine_has_exercise.objects.all()


@api_view(['GET'])
def get_user_routines(request, email):
    queryset = User_has_Routine.objects.all()
    user_routines = queryset.filter(user__email = email)
    depth = 0

    try:
        depth = int(request.query_params.get('depth', 0))
    except ValueError:
        pass # Ignore non-numeric parameters and keep default 0 depth

    serialized = User_has_RoutineSerializer(user_routines, many=True, context={'depth': depth})

    return Response(serialized.data)

@api_view(['GET'])
def get_routine_exercises(request, routine):
    routines_objects = Routine.objects.all()
    routine_object = routines_objects.get(id = routine)
    exercises = routine_object.exercise.all()
    serialized = ExerciseSerializer(exercises, many=True)

    return Response(serialized.data)
