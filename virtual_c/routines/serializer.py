from rest_framework import serializers
from .models import Exercise
from .models import Routine
from .models import User_has_Routine
from .models import Routine_has_exercise


class DynamicDepthSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get('depth', 0)

class ExerciseSerializer(DynamicDepthSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'
        
class Routine_has_exerciseSerializer(DynamicDepthSerializer):
    class Meta:
        model = Routine_has_exercise
        fields = '__all__'
        
# This serializer is used to retrieve a routine with its exercises
# It is for visualization on frontend
class RoutineExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine_has_exercise
        exclude = ['routine']
        depth = 1

class RoutineSerializer(DynamicDepthSerializer):
    exercises = Routine_has_exerciseSerializer(many=True, write_only=True)
    class Meta:
        model = Routine
        fields = '__all__'
    
    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        routine = Routine.objects.create(**validated_data)
        for exercise_data in exercises_data:
            Routine_has_exercise.objects.create(routine=routine, **exercise_data)
        return routine

class User_has_RoutineSerializer(DynamicDepthSerializer):
    class Meta:
        model = User_has_Routine
        fields = '__all__'

