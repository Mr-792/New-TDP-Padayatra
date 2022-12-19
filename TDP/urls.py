
from django.contrib import admin
from django.urls import path
from users.views import UsersAPI,DistrictsAPI,AssembliesAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', UsersAPI.as_view({'post':'login'})),
    path('send-otp', UsersAPI.as_view({'post':'send_otp'})),
    path('verify-otp', UsersAPI.as_view({'post':'verify_otp'})),
    path('signup', UsersAPI.as_view({'post':'signup'})),
    path('all-users', UsersAPI.as_view({'get':'all_users'})),
    path('delete-user/<int:pk>',UsersAPI.as_view({'delete':'destroy'})),

    path('all-districts', DistrictsAPI.as_view({'get':'all_districts'})),
    path('all-assemblies', AssembliesAPI.as_view({'get':'all_assemblies'})),
    # path('create-districts', DistrictsAPI.as_view({'post':'create'})),
    # path('create-assemblies', AssembliesAPI.as_view({'post':'create'})),


    

]
