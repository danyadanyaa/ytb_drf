from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

from api.views import PostView, CommentView, GroupView

router = DefaultRouter()
router.register('posts', PostView)
router.register(r'posts/(?P<id>[^/.]+)/comments', CommentView, basename='comments')
router.register('group', GroupView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(router.urls)),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
]

