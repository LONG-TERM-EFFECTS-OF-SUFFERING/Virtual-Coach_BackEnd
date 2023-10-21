from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from routines import views

router = routers.DefaultRouter()
router.register(r"exercise", views.ExerciseView, "Exercise")
router.register(r"routine", views.RoutineView, "Routine")
router.register(r"User_has_Routine", views.User_has_RoutineView, "User_has_Routine")
# router.register(r"Routine_has_exerciseView", views.Routine_has_exerciseView, "Routine_has_exerciseView")

urlpatterns = [
    path("api/", include(router.urls)),
    path('docs/', include_docs_urls(title='Routine API')),
    path("api/get-user-routines/<str:email>", views.get_user_routines, name='get user routines'),
]
