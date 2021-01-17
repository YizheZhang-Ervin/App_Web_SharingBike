from django.urls import path

from bikesys.views import VerifyApi,CustApi,home,OperApi,MgtApi

app_name = "bikesys"
urlpatterns = [
    path('', home, name='home'),
    path('api/verify/', VerifyApi.as_view(), name='verify'),
    path('api/cust/', CustApi.as_view(), name='cust'),
    path('api/oper/', OperApi.as_view(), name='oper'),
    path('api/mgt/', MgtApi.as_view(), name='mgt'),
]