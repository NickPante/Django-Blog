from django.urls import path
from . import views

app_name='blog'
urlpatterns= [
    #post views
    path('',views.post_list, name='post_list'),#PATH ΓΙΑ ΟΛΑ ΤΑ POST
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),#PATH ΓΙΑ ΣΥΓΚΕΚΡΙΜΕΝΑ POST
    path('<int:post_id>/comment/',views.post_comment, name='post_comment'),#PATH ΓΙΑ ΤΑ ΔΕΔΟΜΕΝΑ ΤΟΥ ΣΧΟΛΙΟΥ
    ]