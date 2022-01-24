from django.urls import path
from Login import views
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index,name="home"),
    path('login',views.loginUser,name="login"),
    path('signin',views.signinUser,name="signin"),
    path('logout',views.logoutUser,name='logout')
]