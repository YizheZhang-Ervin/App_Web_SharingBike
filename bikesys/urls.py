from django.urls import path

from . import views

app_name = "bikesys"
urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path("loginVerify/",views.loginVerify, name="lVerify"),
    path("registerVerify/",views.registerVerify, name="rVerify"),
    path('<int:pk>/', views.userView.as_view(), name='users'),
    path("rent/",views.rent, name="rent"),
    path("back/",views.back, name="back"),
    path("sRepair/",views.submitRepair, name="sRepair"),
    path("repair/",views.repair, name="repair"),
    path("bikeOps/",views.bikeOps,name="bikeOps"),
    path("visual/",views.visual,name="visual"),
]