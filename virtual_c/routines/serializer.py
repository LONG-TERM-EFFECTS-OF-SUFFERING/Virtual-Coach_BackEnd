from rest_framework import serializers
from .models import Exercise
from .models import Routine
from .models import User_has_Routine
from .models import Routine_has_exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = '__all__'

class User_has_RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_has_Routine
        fields = '__all__'

class Routine_has_exerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine_has_exercise
        fields = '__all__'
