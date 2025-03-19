from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("Register.html", views.Register, name="Register"),
	       path("Signup", views.Signup, name="Signup"),
	       path("Login.html", views.Login, name="Login"),
	       path("UserLogin", views.UserLogin, name="UserLogin"),
           path("Uploadimage", views.Uploadimage, name="Uploadimage"),
           path("UploadimageAction", views.UploadimageAction, name="UploadimageAction"),
           path("Result", views.Result, name="Result"),       
]