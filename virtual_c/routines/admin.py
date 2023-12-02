from django.contrib import admin
from .models import Exercise, Routine, User_has_Routine, Routine_has_exercise


admin.site.register(Exercise)
admin.site.register(Routine)
admin.site.register(User_has_Routine)
admin.site.register(Routine_has_exercise)
