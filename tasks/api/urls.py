from django.urls import path
from rest_framework import routers
from tasks.api.resources import TasksViewSet, AddCommentAPIView

router = routers.SimpleRouter()
router.register(r'user_tasks', TasksViewSet)
# router.register(r'orders', OrdersViewSet)
# router.register(r'returns', ReturnViewSet)
urlpatterns = router.urls


urlpatterns += [
    path('add_comment/', AddCommentAPIView.as_view()),
]
