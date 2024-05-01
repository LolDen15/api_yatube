from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet

router_ver1 = SimpleRouter()
router_ver1.register(r'groups', GroupViewSet, 'groups')
router_ver1.register(r'posts', PostViewSet, 'posts')
router_ver1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_ver1.urls)),
]
