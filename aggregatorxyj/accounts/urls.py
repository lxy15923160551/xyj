from django.urls import path
from .views import login_view, register_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    # ... 其他路径
]
