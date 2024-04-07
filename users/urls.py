from django.urls import path, include

from dj_rest_auth.views import LoginView, UserDetailsView, LogoutView

from users.views import SignupAPIView

app_name = 'users'

urlpatterns = [
    path(
        'signup/',
        SignupAPIView.as_view(),
        name='users-signup'
    ),
    path(
        'signin/',
        LoginView.as_view(),
        name='users-signin'
    ),
    path(
        'me/',
        UserDetailsView.as_view(),
        name='user-detail'
    ),
    path(
        'signout/',
        LogoutView.as_view(),
        name='user-logout'
    ),
]
