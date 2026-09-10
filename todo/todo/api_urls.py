from rest_framework.routers import DefaultRouter
from todo.api_views import TodoViewSet

router = DefaultRouter()
router.register("todos", TodoViewSet, basename="todo-api",)

urlpatterns = router.urls
