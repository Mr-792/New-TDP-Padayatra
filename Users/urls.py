from django.urls import path
from Users.views import UsersAPI,DistrictsAPI,AssembliesAPI,PadayatraRegistrationAPI,ProfessionAPI

urlpatterns = [
    path('all-districts', DistrictsAPI.as_view({'get':'all_districts'})),
    path('all-assemblies', AssembliesAPI.as_view({'get':'all_assemblies'})),
    path('all-professions', ProfessionAPI.as_view({'get':'all_professions'})),

    path('search-assemblies/<str:district>', AssembliesAPI.as_view({'get':'search_assemblies'})),
    path('signup', UsersAPI.as_view({'post':'signup'})),
    path('verify-otp', UsersAPI.as_view({'post':'verify_otp'})),
    path('login', UsersAPI.as_view({'post':'login'})),
    path('resend-otp', UsersAPI.as_view({'post':'resend_otp'})),
    path('all-users', UsersAPI.as_view({'get':'all_users'})),
    path('delete-user/<int:pk>',UsersAPI.as_view({'delete':'destroy'})),
    path('download-all-users', UsersAPI.as_view({'get':'download_all_users'})),

    path('create-padayatra-registration', PadayatraRegistrationAPI.as_view({'post':'create'})),
    path('get-padayatra-registration/<int:user_id>', PadayatraRegistrationAPI.as_view({'get':'retrieve'})),
    path('update-padayatra-registration',PadayatraRegistrationAPI.as_view({'put':'update'})),
    path('delete-padayatra-registration',PadayatraRegistrationAPI.as_view({'delete':'destroy'})),

    ]