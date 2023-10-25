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

class RoutineSerializer(DynamicDepthSerializer):
    class Meta:
        model = Routine
        fields = '__all__'

class User_has_RoutineSerializer(DynamicDepthSerializer):
    class Meta:
        model = User_has_Routine
        fields = '__all__'

class Routine_has_exerciseSerializer(DynamicDepthSerializer):
    class Meta:
        model = Routine_has_exercise
        fields = '__all__'
