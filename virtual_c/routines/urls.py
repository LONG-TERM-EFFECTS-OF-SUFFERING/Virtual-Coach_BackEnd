from django.urls import include, path
from rest_framework import routers
from routines import views

router = routers.DefaultRouter()
router.register(r"exercise", views.ExerciseView, "Exercise")
router.register(r"routine", views.RoutineView, "Routine")
router.register(r"User_has_Routine", views.User_has_RoutineView, "User_has_Routine")
router.register(r"Routine_has_exercise", views.Routine_has_exerciseView, "Routine_has_exercise")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/get-user-routines/<int:id>", views.get_user_routines, name='get_user_routines'),
    path("api/get-routine-exercises/<int:routine>", views.get_routine_exercises, name='get_routine_exercises'),
    path("api/edit-routine/<int:routine>", views.edit_routine, name='edit_a_routine'),
]
