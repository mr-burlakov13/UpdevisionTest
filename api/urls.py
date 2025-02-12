from django.urls import path
from .views import SignupView, SigninView, InfoView, LatencyView, LogoutView

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('signin', SigninView.as_view(), name='signin'),
    path('info', InfoView.as_view(), name='info'),
    path('latency', LatencyView.as_view(), name='latency'),
    path('logout', LogoutView.as_view(), name='logout'),
]
