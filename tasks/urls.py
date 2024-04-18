from django.urls import path
from . import views
urlpatterns = [
path('',views.home,name='home'),
path('sigunp/',views.sigunp,name='sigunp'),
path('tasks/',views.tasks,name='tasks'),
path('logout/',views.signout,name='logout'),
path('signin/',views.signin,name='signin')
]