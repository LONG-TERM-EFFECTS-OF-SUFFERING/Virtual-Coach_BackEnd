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
    id = serializers.IntegerField(required=False)
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
    time = serializers.IntegerField(required=False)
    exercises_number = serializers.IntegerField(required=False)

    class Meta:
        model = Routine
        fields = '__all__'
        
    def update_or_add_exercises(self, instance, exercises):
        created_instances = []
        edited_instances = []
        for exercise in exercises:
            exercise['routine'] = instance
            try:
                exercise_instance, created = Routine_has_exercise.objects.update_or_create(pk=exercise.get('id'), defaults=exercise)
                if created:
                    created_instances.append(exercise_instance)
                else:
                    edited_instances.append(exercise_instance)
            except Exception as e:
                raise serializers.ValidationError({'error': str(e)})
                
        return (created_instances, edited_instances)

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        routine = Routine.objects.create(**validated_data)

        for exercise_data in exercises_data:
            Routine_has_exercise.objects.create(routine=routine, **exercise_data)

        return routine
    
    def update(self, instance, validated_data):
        exercises = validated_data.pop('exercises', [])
        created_instances, edited_instances = self.update_or_add_exercises(instance, exercises)
            
        fields = ['name', 'description', 'time', 'exercises_number']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError: # validated_data may not contain all fields during PATCH
                pass
        instance.save()
        return instance

class User_has_RoutineSerializer(DynamicDepthSerializer):
    class Meta:
        model = User_has_Routine
        fields = '__all__'

