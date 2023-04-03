from django.urls import path
from rest_framework import routers
from tasks.api.resources import TasksViewSet, AddCommentAPIView, AdminAcceptDeclineTaskAPIView, AdminTasksListAPIView, \
    TaskReclaimAPIView, Tested, AdminReClaimedTasksAPIView

router = routers.SimpleRouter()
router.register(r'user_tasks', TasksViewSet)
# router.register(r'orders', OrdersViewSet)
urlpatterns = router.urls


urlpatterns += [
    path('add_comment/', AddCommentAPIView.as_view()),
    # user path
    path('task_reclaim/<int:pk>/', TaskReclaimAPIView.as_view()),
    # admin path
    path('admin_tasks/', AdminTasksListAPIView.as_view()),
    path('admin_reclaimed_tasks/', AdminReClaimedTasksAPIView.as_view()),
    path('accept_or_decline/<int:pk>/', AdminAcceptDeclineTaskAPIView.as_view()),
    path('test/', Tested.as_view())
]
