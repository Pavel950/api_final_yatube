from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = SimpleRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register(
    r'posts/(?P<post_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('follow', FollowViewSet, basename='followers')
router_v1.register('groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
