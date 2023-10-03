from django.urls import path, include
from user.views import RegisterView, LoginView, PostView
from rest_framework import routers
from .views import UserViewSet, PublicUserListView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)




urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('post/', PostView.as_view()),
    path('publicUsers/', PublicUserListView.as_view(), name='user-list'),

    path('', include(router.urls)),

    
    
]
