from django.urls import path, include
from . import views
urlpatterns = [
    path('',include('django.contrib.auth.urls')),#PATH ΓΙΑ ΤΑ ΕΝΣΩΜΑΤΟΠΟΙΗΜΕΝΑ ΠΧ LOGIN SIGNUP
    path('register/',views.register,name='register'),#PATH ΓΙΑ ΤΗΝ ΕΓΓΡΑΦΗ
]