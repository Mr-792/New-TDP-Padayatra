from django.urls import path
from . import views


urlpatterns=[
    path('upload/',views.UploadPost),
    path('upload-file',views.PostsApi.as_view({'post':'upload'}))

]