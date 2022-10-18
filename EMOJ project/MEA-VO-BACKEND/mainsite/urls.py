from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("randomproblem/<str:category>/<str:level>/", views.randomproblem, name="ramdompronlem"),
    path("getproblem/<str:problem>/", views.getproblem, name='getproblem'),
    path("problemlist/", views.problemlist, name="problemlist"),
    path("leaderboard/", views.userleaderboard, name='leaderboard'),
    path('userinfo/<str:user>/', views.getuserinfo, name="userinfo"),
    path("solveproblem/<str:problem>/", views.solveproblem, name="solveproblem"),
    path("makeproblem/", views.makeproblem, name="makeproblem"),
    path("makepost/", views.makepost, name="makepost"),
    path("editprofile/", views.editprofile, name="editprofile"),
    path("fileupload/", views.storeAndProcessFile, name="file"),
    path('image/<str:imgid>', views.image, name='image'),
    path('edit/<str:name>', views.edit_entry, name='editentry'),
    path('edited', views.edited, name='edited')

]
